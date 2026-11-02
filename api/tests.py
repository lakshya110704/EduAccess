from datetime import timedelta
from decimal import Decimal
from unittest import skipUnless

from django.db import IntegrityError, connection, transaction
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from .models import (
    AcademicBlock,
    Appointment,
    CustomUser,
    FacultyBlock,
    MyProfessor,
    Notification,
    format_cabin,
    parse_cabin,
)


def make_user(username, role, **extra):
    return CustomUser.objects.create_user(username=username, password='pass-1234-word', role=role, **extra)


class BaseTestCase(TestCase):
    def setUp(self):
        self.student = make_user('stu', 'student')
        self.other_student = make_user('stu2', 'student')
        self.prof = make_user(
            'prof', 'professor', first_name='Ada', last_name='Lovelace', academic_block=2, faculty_block=3, cabin='106'
        )
        self.other_prof = make_user('prof2', 'professor')
        # Tomorrow, rounded down to a quarter hour (bookings must start on :00/:15/:30/:45).
        self.future = (timezone.now() + timedelta(days=1)).replace(second=0, microsecond=0)
        self.future -= timedelta(minutes=self.future.minute % 15)
        self.client = APIClient()

    def as_user(self, user):
        self.client.force_authenticate(user)
        return self.client

    def book(self, student=None, professor=None, when=None, slots=1, status='Pending'):
        return Appointment.objects.create(
            student=student or self.student,
            professor=professor or self.prof,
            appointment_time=when or self.future,
            slots=slots,
            status=status,
        )


class ProfessorDirectoryTests(BaseTestCase):
    def test_requires_login(self):
        self.assertEqual(self.client.get('/api/professors/').status_code, 403)

    def test_list_is_my_professors_with_public_fields(self):
        client = self.as_user(self.student)
        self.assertEqual(client.get('/api/professors/').json(), [])
        client.post(f'/api/professors/{self.prof.id}/mine/')
        resp = client.get('/api/professors/')
        self.assertEqual([p['username'] for p in resp.json()], ['prof'])
        self.assertTrue(resp.json()[0]['is_mine'])
        self.assertNotIn('email', resp.json()[0])

    def test_search_by_name_returns_cabin(self):
        resp = self.as_user(self.student).get('/api/professors/?search=lovelace')
        self.assertEqual([(p['username'], p['cabin_label']) for p in resp.json()], [('prof', 'AB2 FB3 : 106')])

    def test_directory_is_read_only(self):
        client = self.as_user(self.student)
        self.assertEqual(
            client.patch(f'/api/professors/{self.prof.id}/', {'availability_status': 'Free'}).status_code, 405
        )
        self.assertEqual(client.delete(f'/api/professors/{self.prof.id}/').status_code, 405)
        self.assertEqual(client.post('/api/professors/', {'username': 'x'}).status_code, 405)


class MeTests(BaseTestCase):
    def test_professor_updates_own_availability(self):
        resp = self.as_user(self.prof).patch('/api/me/', {'availability_status': 'Free'}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.prof.refresh_from_db()
        self.assertEqual(self.prof.availability_status, 'Free')

    def test_role_and_username_are_read_only(self):
        self.as_user(self.student).patch('/api/me/', {'role': 'professor', 'username': 'hacker'}, format='json')
        self.student.refresh_from_db()
        self.assertEqual((self.student.role, self.student.username), ('student', 'stu'))

    def test_student_cannot_set_availability(self):
        resp = self.as_user(self.student).patch('/api/me/', {'availability_status': 'Free'}, format='json')
        self.assertEqual(resp.status_code, 400)

    def test_invalid_status_rejected(self):
        resp = self.as_user(self.prof).patch('/api/me/', {'availability_status': 'Asleep'}, format='json')
        self.assertEqual(resp.status_code, 400)


class BookingTests(BaseTestCase):
    def post(self, user, **data):
        payload = {'professor': self.prof.id, 'appointment_time': self.future.isoformat()}
        payload.update(data)
        return self.as_user(user).post('/api/appointments/', payload, format='json')

    def test_student_books_and_professor_is_notified(self):
        resp = self.post(self.student)
        self.assertEqual(resp.status_code, 201, resp.content)
        appt = Appointment.objects.get()
        self.assertEqual((appt.student, appt.status), (self.student, 'Pending'))
        self.assertTrue(Notification.objects.filter(user=self.prof).exists())

    def test_student_field_and_status_cannot_be_forged(self):
        resp = self.post(self.student, student=self.other_student.id, status='Confirmed')
        self.assertEqual(resp.status_code, 201)
        appt = Appointment.objects.get()
        self.assertEqual((appt.student, appt.status), (self.student, 'Pending'))

    def test_professor_cannot_book(self):
        self.assertEqual(self.post(self.prof, professor=self.other_prof.id).status_code, 403)

    def test_cannot_book_a_non_professor(self):
        self.assertEqual(self.post(self.student, professor=self.other_student.id).status_code, 400)

    def test_cannot_book_in_the_past(self):
        past = (timezone.now() - timedelta(hours=1)).isoformat()
        self.assertEqual(self.post(self.student, appointment_time=past).status_code, 400)

    def test_pending_requests_for_the_same_slot_are_allowed(self):
        self.book(student=self.other_student)
        self.assertEqual(self.post(self.student).status_code, 201)

    def test_cannot_request_a_confirmed_slot(self):
        self.book(student=self.other_student, status='Confirmed')
        self.assertEqual(self.post(self.student).status_code, 400)

    def test_can_rebook_a_cancelled_slot(self):
        appt = self.book(student=self.other_student)
        appt.status = 'Cancelled'
        appt.save()
        self.assertEqual(self.post(self.student).status_code, 201)


class AppointmentAccessTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.appt = self.book()
        self.url = f'/api/appointments/{self.appt.id}/'

    def patch(self, user, status):
        return self.as_user(user).patch(self.url, {'status': status}, format='json')

    def test_users_only_see_their_own_appointments(self):
        self.assertEqual(len(self.as_user(self.student).get('/api/appointments/').json()), 1)
        self.assertEqual(len(self.as_user(self.prof).get('/api/appointments/').json()), 1)
        self.assertEqual(len(self.as_user(self.other_student).get('/api/appointments/').json()), 0)
        self.assertEqual(len(self.as_user(self.other_prof).get('/api/appointments/').json()), 0)
        self.assertEqual(self.as_user(self.other_student).get(self.url).status_code, 404)

    def test_professor_confirms_and_student_is_notified(self):
        resp = self.patch(self.prof, 'Confirmed')
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertEqual(resp.json()['status'], 'Confirmed')
        self.assertTrue(Notification.objects.filter(user=self.student, message__contains='Confirmed').exists())

    def test_student_cannot_confirm_own_appointment(self):
        self.assertEqual(self.patch(self.student, 'Confirmed').status_code, 400)
        self.appt.refresh_from_db()
        self.assertEqual(self.appt.status, 'Pending')

    def test_student_can_cancel_and_professor_is_notified(self):
        self.assertEqual(self.patch(self.student, 'Cancelled').status_code, 200)
        self.assertTrue(Notification.objects.filter(user=self.prof, message__contains='Cancelled').exists())

    def test_cancelled_is_final(self):
        self.patch(self.student, 'Cancelled')
        self.assertEqual(self.patch(self.prof, 'Confirmed').status_code, 400)

    def test_other_users_cannot_touch_it(self):
        self.assertEqual(self.patch(self.other_prof, 'Confirmed').status_code, 404)
        self.assertEqual(self.patch(self.other_student, 'Cancelled').status_code, 404)

    def test_only_status_is_editable(self):
        later = (self.future + timedelta(days=3)).isoformat()
        self.as_user(self.prof).patch(
            self.url,
            {'status': 'Confirmed', 'student': self.other_student.id, 'appointment_time': later},
            format='json',
        )
        self.appt.refresh_from_db()
        self.assertEqual(self.appt.student, self.student)
        self.assertEqual(self.appt.appointment_time, self.future)

    def test_no_delete_or_put(self):
        client = self.as_user(self.prof)
        self.assertEqual(client.delete(self.url).status_code, 405)
        self.assertEqual(client.put(self.url, {'status': 'Confirmed'}, format='json').status_code, 405)


class NotificationTests(BaseTestCase):
    def test_requires_login(self):
        self.assertEqual(self.client.get('/api/notifications/').status_code, 403)

    def test_only_own_notifications(self):
        Notification.objects.create(user=self.student, message='mine')
        Notification.objects.create(user=self.other_student, message='theirs')
        resp = self.as_user(self.student).get('/api/notifications/')
        self.assertEqual([n['message'] for n in resp.json()], ['mine'])


class PageTests(BaseTestCase):
    def login(self, username, role='student', **extra):
        return self.client.post('/login/', {'role': role, 'username': username, 'password': 'pass-1234-word', **extra})

    def test_student_login_with_matching_role(self):
        self.assertRedirects(self.login('stu'), '/student/', fetch_redirect_response=False)

    def test_professor_login(self):
        self.assertRedirects(self.login('prof', role='professor'), '/professor/', fetch_redirect_response=False)

    def test_wrong_role_is_refused_with_hint(self):
        resp = self.login('stu', role='professor')
        self.assertContains(resp, 'This is a student account. Is the role selected right?', status_code=403)
        self.assertNotIn('_auth_user_id', self.client.session)
        resp = self.login('prof', role='student')
        self.assertContains(resp, 'This is a professor account.', status_code=403)

    def test_role_is_required(self):
        resp = self.client.post('/login/', {'username': 'stu', 'password': 'pass-1234-word'})
        self.assertContains(resp, 'Select your role.', status_code=400)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_bad_password_message_is_neutral(self):
        # Same message whatever role is selected, so a guesser learns nothing about the account.
        for role in ('student', 'professor'):
            resp = self.client.post('/login/', {'role': role, 'username': 'stu', 'password': 'nope'})
            self.assertContains(
                resp,
                'Invalid username or password for the selected role. Check that the right role is selected.',
                status_code=401,
            )
        resp = self.client.post('/login/', {'role': 'student', 'username': 'no-such-user', 'password': 'nope'})
        self.assertEqual(resp.status_code, 401)

    def test_selected_role_kept_after_failure(self):
        resp = self.client.post('/login/', {'role': 'professor', 'username': 'x', 'password': 'y'})
        self.assertContains(resp, 'id="role-professor" value="professor" checked', status_code=401)

    def test_user_without_role_is_not_logged_in(self):
        make_user('nobody', '')
        resp = self.login('nobody')
        self.assertContains(resp, 'This account cannot sign in here.', status_code=403)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_unsafe_next_is_ignored(self):
        resp = self.login('stu', next='https://evil.example.com/')
        self.assertRedirects(resp, '/student/', fetch_redirect_response=False)

    def test_dashboards_require_login(self):
        self.assertRedirects(self.client.get('/professor/'), '/login/?next=/professor/', fetch_redirect_response=False)
        self.assertRedirects(self.client.get('/student/'), '/login/?next=/student/', fetch_redirect_response=False)

    def test_dashboards_enforce_role(self):
        self.client.force_login(self.student)
        self.assertEqual(self.client.get('/professor/').status_code, 403)
        self.assertEqual(self.client.get('/student/').status_code, 200)
        self.client.force_login(self.prof)
        self.assertEqual(self.client.get('/student/').status_code, 403)
        self.assertEqual(self.client.get('/professor/').status_code, 200)

    def test_logout_requires_post(self):
        self.client.force_login(self.student)
        self.assertEqual(self.client.get('/logout/').status_code, 405)
        self.client.post('/logout/')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_healthz(self):
        self.assertEqual(self.client.get('/healthz/').json(), {'status': 'ok'})


class AdminUserCreationTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.admin = CustomUser.objects.create_superuser(username='boss', password='pass-1234-word')
        self.client.force_login(self.admin)

    def test_add_page_shows_profile_fields(self):
        resp = self.client.get('/admin/api/customuser/add/')
        for field in ('role', 'academic_block', 'faculty_block', 'cabin', 'availability_status', 'first_name'):
            self.assertContains(resp, f'name="{field}"')

    def test_professor_created_in_one_step(self):
        resp = self.client.post(
            '/admin/api/customuser/add/',
            {
                'username': 'newprof',
                'usable_password': 'true',
                'password1': 'a-long-unusual-pass-77',
                'password2': 'a-long-unusual-pass-77',
                'first_name': 'Neha',
                'last_name': 'Iyer',
                'role': 'professor',
                'academic_block': '1',
                'faculty_block': '2',
                'cabin': '210',
                'availability_status': 'Busy',
            },
        )
        self.assertEqual(resp.status_code, 302, resp.content[:500])
        prof = CustomUser.objects.get(username='newprof')
        self.assertEqual(
            (prof.role, prof.cabin_label, prof.availability_status), ('professor', 'AB1 FB2 : 210', 'Busy')
        )
        self.assertTrue(prof.check_password('a-long-unusual-pass-77'))


class SignupTests(TestCase):
    password = 'a-long-unusual-pass-77'

    def data(self, **overrides):
        data = {
            'role': 'student',
            'username': 'riya',
            'first_name': 'Riya',
            'middle_name': 'K',
            'last_name': 'Sharma',
            'email': 'Riya.Sharma@muj.manipal.edu',
            'college_id': 'ab12345',
            'password1': self.password,
            'password2': self.password,
        }
        data.update(overrides)
        return data

    def test_student_signup_creates_inactive_account(self):
        resp = self.client.post('/signup/', self.data())
        self.assertRedirects(resp, '/signup/done/', fetch_redirect_response=False)
        user = CustomUser.objects.get(username='riya')
        self.assertFalse(user.is_active)
        self.assertEqual(
            (user.role, user.email, user.college_id, user.get_full_name()),
            ('student', 'riya.sharma@muj.manipal.edu', 'AB12345', 'Riya K Sharma'),
        )
        self.assertTrue(user.check_password(self.password))

    def test_professor_signup_uses_faculty_domain(self):
        resp = self.client.post(
            '/signup/', self.data(role='professor', username='neha', email='neha@jaipur.manipal.edu', college_id='E900')
        )
        self.assertEqual(resp.status_code, 302, resp.content[:300])
        self.assertEqual(CustomUser.objects.get(username='neha').role, 'professor')

    def test_email_domain_must_match_role(self):
        for role, email in [
            ('student', 'riya@jaipur.manipal.edu'),
            ('professor', 'riya@muj.manipal.edu'),
            ('student', 'riya@gmail.com'),
            ('student', 'riya@evil-muj.manipal.edu'),
        ]:
            resp = self.client.post('/signup/', self.data(role=role, email=email))
            self.assertEqual(resp.status_code, 200, (role, email))
            self.assertContains(resp, 'must register with their @')
        self.assertFalse(CustomUser.objects.exists())

    def test_cannot_request_admin_role(self):
        resp = self.client.post('/signup/', self.data(role='admin'))
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(CustomUser.objects.exists())

    def test_duplicates_rejected(self):
        self.client.post('/signup/', self.data())
        resp = self.client.post('/signup/', self.data(username='riya2', email='RIYA.sharma@muj.manipal.edu'))
        self.assertContains(resp, 'An account with this email already exists.')
        resp = self.client.post(
            '/signup/', self.data(username='riya3', email='other@muj.manipal.edu', college_id='AB12345')
        )
        self.assertContains(resp, 'An account with this roll number already exists.')
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_same_id_allowed_across_roles(self):
        self.client.post('/signup/', self.data(college_id='X1'))
        resp = self.client.post(
            '/signup/', self.data(role='professor', username='p', email='p@jaipur.manipal.edu', college_id='X1')
        )
        self.assertEqual(resp.status_code, 302)

    def test_password_mismatch_and_required_fields(self):
        resp = self.client.post('/signup/', self.data(password2='different-pass-99'))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post('/signup/', self.data(first_name='', college_id=''))
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(CustomUser.objects.exists())

    def test_pending_account_sees_approval_message(self):
        self.client.post('/signup/', self.data())
        resp = self.client.post('/login/', {'role': 'student', 'username': 'riya', 'password': self.password})
        self.assertContains(resp, 'awaiting approval', status_code=403)
        resp = self.client.post('/login/', {'role': 'professor', 'username': 'riya', 'password': self.password})
        self.assertContains(resp, 'This is a student account.', status_code=403)
        resp = self.client.post('/login/', {'role': 'student', 'username': 'riya', 'password': 'wrong-password'})
        self.assertContains(resp, 'Invalid username or password', status_code=401)

    def test_admin_activation_then_login(self):
        self.client.post('/signup/', self.data())
        admin_user = CustomUser.objects.create_superuser(username='boss', password='pass-1234-word')
        self.client.force_login(admin_user)
        user = CustomUser.objects.get(username='riya')
        self.client.post(
            '/admin/api/customuser/', {'action': 'activate_accounts', '_selected_action': [user.pk]}, follow=True
        )
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.client.logout()
        resp = self.client.post('/login/', {'role': 'student', 'username': 'riya', 'password': self.password})
        self.assertRedirects(resp, '/student/', fetch_redirect_response=False)

    def test_signup_page_renders_and_login_links_to_it(self):
        self.assertContains(self.client.get('/signup/'), 'name="college_id"')
        login_page = self.client.get('/login/')
        self.assertContains(login_page, 'href="/signup/"')
        self.assertContains(login_page, 'name="role"')


class AdminSeparationTests(BaseTestCase):
    def test_admin_login_is_branded(self):
        resp = self.client.get('/admin/login/')
        self.assertContains(resp, 'EduAccess Admin')
        self.assertContains(resp, 'Staff sign-in')
        self.assertNotContains(resp, 'Django administration')

    def test_public_login_has_no_admin_link(self):
        self.assertNotContains(self.client.get('/login/'), '/admin/')

    def test_admin_logout_returns_to_admin_login(self):
        admin_user = CustomUser.objects.create_superuser(username='boss', password='pass-1234-word')
        self.client.force_login(admin_user)
        self.assertRedirects(self.client.post('/admin/logout/'), '/admin/login/', fetch_redirect_response=False)

    def test_app_logout_still_returns_to_app_login(self):
        self.client.force_login(self.student)
        self.assertRedirects(self.client.post('/logout/'), '/login/', fetch_redirect_response=False)


class ThemeAndSwitchTests(BaseTestCase):
    def test_login_and_signup_render_the_role_switch(self):
        for url in ('/login/', '/signup/'):
            resp = self.client.get(url)
            self.assertContains(resp, 'class="role-switch"')
            self.assertContains(resp, 'id="role-student" value="student" checked')
            self.assertContains(resp, 'id="role-professor" value="professor"')
            self.assertContains(resp, 'data-theme="student"')

    def test_failed_professor_login_keeps_professor_theme(self):
        resp = self.client.post('/login/', {'role': 'professor', 'username': 'x', 'password': 'y'})
        self.assertContains(resp, 'id="role-professor" value="professor" checked', status_code=401)
        self.assertContains(resp, 'data-theme="professor"', status_code=401)

    def test_dashboards_keep_their_role_theme(self):
        self.client.force_login(self.student)
        self.assertContains(self.client.get('/student/'), 'data-theme="student"')
        self.client.force_login(self.prof)
        self.assertContains(self.client.get('/professor/'), 'data-theme="professor"')


class MyProfessorTests(BaseTestCase):
    def test_add_and_remove(self):
        client = self.as_user(self.student)
        self.assertEqual(client.post(f'/api/professors/{self.prof.id}/mine/').status_code, 200)
        client.post(f'/api/professors/{self.prof.id}/mine/')  # adding twice is harmless
        self.assertEqual(MyProfessor.objects.filter(student=self.student).count(), 1)
        self.assertEqual(client.delete(f'/api/professors/{self.prof.id}/mine/').status_code, 200)
        self.assertEqual(client.get('/api/professors/').json(), [])

    def test_lists_are_per_student(self):
        self.as_user(self.student).post(f'/api/professors/{self.prof.id}/mine/')
        self.assertEqual(self.as_user(self.other_student).get('/api/professors/').json(), [])

    def test_search_covers_everyone_and_flags_mine(self):
        client = self.as_user(self.student)
        client.post(f'/api/professors/{self.prof.id}/mine/')
        results = {p['username']: p['is_mine'] for p in client.get('/api/professors/?search=prof').json()}
        self.assertEqual(results, {'prof': True, 'prof2': False})

    def test_search_never_returns_students(self):
        results = self.as_user(self.student).get('/api/professors/?search=stu').json()
        self.assertEqual(results, [])

    def test_search_needs_two_characters(self):
        resp = self.as_user(self.student).get('/api/professors/?search=a')
        self.assertEqual(resp.status_code, 400)

    def test_search_is_capped(self):
        for i in range(25):
            make_user(f'bulkprof{i}', 'professor')
        self.assertEqual(len(self.as_user(self.student).get('/api/professors/?search=bulkprof').json()), 20)

    def test_only_students_can_follow(self):
        resp = self.as_user(self.prof).post(f'/api/professors/{self.other_prof.id}/mine/')
        self.assertEqual(resp.status_code, 403)

    def test_cannot_follow_a_student(self):
        resp = self.as_user(self.student).post(f'/api/professors/{self.other_student.id}/mine/')
        self.assertEqual(resp.status_code, 404)

    def test_can_book_a_professor_not_in_my_list(self):
        resp = self.as_user(self.student).post(
            '/api/appointments/',
            {'professor': self.other_prof.id, 'appointment_time': self.future.isoformat()},
            format='json',
        )
        self.assertEqual(resp.status_code, 201, resp.content)


class BookingRuleTests(BaseTestCase):
    def post(self, when, slots=1, student=None):
        return self.as_user(student or self.student).post(
            '/api/appointments/',
            {'professor': self.prof.id, 'appointment_time': when.isoformat(), 'slots': slots},
            format='json',
        )

    def confirm(self, appt):
        return self.as_user(self.prof).patch(f'/api/appointments/{appt.id}/', {'status': 'Confirmed'}, format='json')

    def test_must_start_on_quarter_hour(self):
        self.assertEqual(self.post(self.future + timedelta(minutes=7)).status_code, 400)
        self.assertEqual(self.post(self.future + timedelta(minutes=15)).status_code, 201)

    def test_one_or_two_slots(self):
        resp = self.post(self.future, slots=2)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(Appointment.objects.get().end_time, self.future + timedelta(minutes=30))
        self.assertEqual(self.post(self.future + timedelta(hours=2), slots=3).status_code, 400)

    def test_overlap_with_confirmed_is_refused_but_adjacent_is_fine(self):
        self.book(student=self.other_student, slots=2, status='Confirmed')  # covers future .. future+30
        self.assertEqual(self.post(self.future + timedelta(minutes=15)).status_code, 400)
        self.assertEqual(self.post(self.future + timedelta(minutes=30)).status_code, 201)

    def test_confirming_declines_overlapping_requests_and_notifies(self):
        mine = self.book(slots=2)
        clash = self.book(student=self.other_student, when=self.future + timedelta(minutes=15))
        later = self.book(student=self.other_student, when=self.future + timedelta(minutes=30))
        self.assertEqual(self.confirm(mine).status_code, 200)
        clash.refresh_from_db()
        later.refresh_from_db()
        self.assertEqual((clash.status, later.status), ('Cancelled', 'Pending'))
        note = Notification.objects.get(user=self.other_student)
        self.assertIn('was taken. Please pick another slot.', note.message)

    def test_cannot_confirm_over_another_confirmed(self):
        self.book(student=self.other_student, status='Confirmed')
        pending = self.book()
        resp = self.confirm(pending)
        self.assertContains(resp, 'overlaps another confirmed appointment', status_code=400)

    def test_notification_times_are_local(self):
        appt = self.book()
        self.confirm(appt)
        local = timezone.localtime(appt.appointment_time)
        self.assertIn(f'{local:%H:%M}', Notification.objects.get(user=self.student).message)

    @skipUnless(connection.vendor == 'postgresql', 'exclusion constraint is PostgreSQL-only')
    def test_database_refuses_overlapping_confirmations(self):
        self.book(status='Confirmed')
        with self.assertRaises(IntegrityError), transaction.atomic():
            self.book(student=self.other_student, when=self.future + timedelta(minutes=10), status='Confirmed')


class OpenTimeTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        # A 60-minute window later today, starting at least 15 minutes from now on a quarter hour (local time).
        # Near midnight there is no such window left today, so these tests are skipped then.
        now = timezone.localtime().replace(second=0, microsecond=0)
        start = now + timedelta(minutes=15 + (15 - now.minute % 15) % 15)
        end = start + timedelta(minutes=60)
        if end.date() != now.date():
            self.skipTest('too close to midnight for a same-day open-time window')
        self.open_start, self.open_end = start, end

    def add(self, start=None, end=None, user=None):
        return self.as_user(user or self.prof).post(
            '/api/open-times/',
            {'start': (start or self.open_start).isoformat(), 'end': (end or self.open_end).isoformat()},
            format='json',
        )

    def test_professor_sets_open_time_and_students_see_it(self):
        self.assertEqual(self.add().status_code, 201)
        client = self.as_user(self.student)
        client.post(f'/api/professors/{self.prof.id}/mine/')
        open_today = client.get('/api/professors/').json()[0]['open_today']
        self.assertEqual(len(open_today), 1)

    def test_only_professors_can_set_open_time(self):
        self.assertEqual(self.add(user=self.student).status_code, 403)

    def test_must_be_today_on_quarter_hours(self):
        self.assertEqual(self.add(start=self.open_start + timedelta(minutes=5)).status_code, 400)
        tomorrow = self.open_start + timedelta(days=1)
        self.assertEqual(self.add(start=tomorrow, end=tomorrow + timedelta(hours=1)).status_code, 400)
        self.assertEqual(self.add(end=self.open_start).status_code, 400)

    def test_no_overlapping_windows(self):
        self.add()
        # A window inside the first one (stays within today even late in the evening).
        resp = self.add(start=self.open_start + timedelta(minutes=15), end=self.open_end - timedelta(minutes=15))
        self.assertContains(resp, 'overlaps open time', status_code=400)

    def test_cannot_cover_a_confirmed_appointment(self):
        self.book(when=self.open_start, status='Confirmed')
        self.assertContains(self.add(), 'confirmed appointment in that time', status_code=400)

    def test_open_time_declines_covered_pending_requests(self):
        covered = self.book(when=self.open_start)
        self.assertEqual(self.add().status_code, 201)
        covered.refresh_from_db()
        self.assertEqual(covered.status, 'Cancelled')
        self.assertIn('walk-ins', Notification.objects.get(user=self.student).message)

    def test_no_bookings_inside_open_time(self):
        self.add()
        resp = self.as_user(self.student).post(
            '/api/appointments/',
            {'professor': self.prof.id, 'appointment_time': self.open_start.isoformat()},
            format='json',
        )
        self.assertContains(resp, 'open (walk-in) time', status_code=400)

    def test_professor_lists_and_removes_own_windows(self):
        window_id = self.add().json()['id']
        self.assertEqual(len(self.as_user(self.prof).get('/api/open-times/').json()), 1)
        self.assertEqual(self.as_user(self.other_prof).delete(f'/api/open-times/{window_id}/').status_code, 404)
        self.assertEqual(self.as_user(self.prof).delete(f'/api/open-times/{window_id}/').status_code, 204)


class DashboardLayoutTests(BaseTestCase):
    def sections(self, html):
        import re

        return re.findall(r'<section id="([^"]+)"', html)

    def test_student_dashboard_is_three_sections_plus_dialogs(self):
        self.client.force_login(self.student)
        html = self.client.get('/student/').content.decode()
        self.assertEqual(self.sections(html), ['availability', 'my-appointments', 'notifications'])
        self.assertIn('id="find-dialog"', html)
        self.assertIn('id="book-dialog"', html)
        self.assertIn('data-open-dialog="find-dialog"', html)

    def test_professor_dashboard_is_appointments_and_notifications(self):
        self.client.force_login(self.prof)
        html = self.client.get('/professor/').content.decode()
        self.assertEqual(self.sections(html), ['appointments', 'notifications'])
        self.assertIn('id="open-time-dialog"', html)
        self.assertIn('class="segmented status-switch"', html)


class CabinLocationTests(BaseTestCase):
    def test_parse_and_format(self):
        self.assertEqual(parse_cabin('AB2 FB3 : 106'), (2, 3, '106'))
        self.assertEqual(parse_cabin('FB3 AB2 : 106'), (2, 3, '106'))
        self.assertEqual(parse_cabin('ab2fb3:106a'), (2, 3, '106A'))
        self.assertEqual(parse_cabin('fb3ab2:106a'), (2, 3, '106A'))
        self.assertIsNone(parse_cabin('A-105'))
        self.assertEqual(format_cabin(2, 3, '106'), 'AB2 FB3 : 106')
        self.assertEqual(format_cabin(None, None, '106'), '106')
        self.assertEqual(format_cabin(None, None, ''), '')

    def search(self, query):
        resp = self.as_user(self.student).get('/api/professors/', {'search': query})
        return sorted(p['username'] for p in resp.json())

    def test_search_by_cabin_parts(self):
        make_user('prof3', 'professor', academic_block=2, faculty_block=1, cabin='204')
        self.assertEqual(self.search('AB2 FB3 : 106'), ['prof'])
        self.assertEqual(self.search('FB3 AB2 : 106'), ['prof'])
        self.assertEqual(self.search('AB2'), ['prof', 'prof3'])
        self.assertEqual(self.search('fb1'), ['prof3'])
        self.assertEqual(self.search('106'), ['prof'])
        self.assertEqual(self.search('AB2 lovelace'), ['prof'])


class DirectionsTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.block = AcademicBlock.objects.create(
            number=2,
            latitude=Decimal('26.844100'),
            longitude=Decimal('75.565493'),
            view_360_url='https://example.com/ab2',
        )
        FacultyBlock.objects.create(
            academic_block=self.block, number=3, floor=1, directions='Take the right staircase.\nFB3 is the left wing.'
        )

    def test_full_directions_page(self):
        resp = self.client.get('/go/AB2/FB3/106/')
        self.assertContains(resp, 'Cabin AB2 FB3 : 106')
        self.assertContains(
            resp, 'https://www.google.com/maps/dir/?api=1&amp;destination=26.844100,75.565493&amp;travelmode=walking'
        )
        self.assertContains(resp, 'https://example.com/ab2')
        self.assertContains(resp, 'Floor 1')
        self.assertContains(resp, 'Take the right staircase.<br>FB3 is the left wing.')
        self.assertContains(resp, 'https://wa.me/?text=')

    def test_page_needs_no_login_and_shows_no_names(self):
        resp = self.client.get('/go/AB2/FB3/106/')  # anonymous
        self.assertEqual(resp.status_code, 200)
        self.assertNotContains(resp, 'Lovelace')
        self.assertNotContains(resp, 'prof')

    def test_missing_data_degrades_gracefully(self):
        resp = self.client.get('/go/AB9/FB1/12/')
        self.assertContains(resp, "aren't set up yet")
        self.assertContains(resp, "aren't written yet")
        self.assertContains(resp, '<strong>cabin 12</strong>')

    def test_ground_floor_label(self):
        FacultyBlock.objects.create(academic_block=self.block, number=4, floor=0, directions='Straight ahead.')
        self.assertContains(self.client.get('/go/AB2/FB4/1/'), 'Ground floor')

    def test_professor_api_links_to_directions(self):
        client = self.as_user(self.student)
        client.post(f'/api/professors/{self.prof.id}/mine/')
        self.assertEqual(client.get('/api/professors/').json()[0]['directions_url'], '/go/AB2/FB3/106/')
        self.assertEqual(
            self.as_user(self.student).get('/api/professors/?search=prof2').json()[0]['directions_url'], ''
        )

    def test_admin_edits_blocks_inline(self):
        admin_user = CustomUser.objects.create_superuser(username='boss', password='pass-1234-word')
        self.client.force_login(admin_user)
        resp = self.client.get(f'/admin/api/academicblock/{self.block.id}/change/')
        self.assertContains(resp, 'faculty_blocks-0-directions')

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from .models import Appointment, CustomUser, Notification


def make_user(username, role, **extra):
    return CustomUser.objects.create_user(username=username, password='pass-1234-word', role=role, **extra)


class BaseTestCase(TestCase):
    def setUp(self):
        self.student = make_user('stu', 'student')
        self.other_student = make_user('stu2', 'student')
        self.prof = make_user('prof', 'professor', first_name='Ada', last_name='Lovelace', cabin_number='A-105')
        self.other_prof = make_user('prof2', 'professor')
        self.future = timezone.now() + timedelta(days=1)
        self.client = APIClient()

    def as_user(self, user):
        self.client.force_authenticate(user)
        return self.client

    def book(self, student=None, professor=None, when=None):
        return Appointment.objects.create(
            student=student or self.student, professor=professor or self.prof, appointment_time=when or self.future
        )


class ProfessorDirectoryTests(BaseTestCase):
    def test_requires_login(self):
        self.assertEqual(self.client.get('/api/professors/').status_code, 403)

    def test_lists_only_professors_with_public_fields(self):
        resp = self.as_user(self.student).get('/api/professors/')
        self.assertEqual(resp.status_code, 200)
        usernames = {p['username'] for p in resp.json()}
        self.assertEqual(usernames, {'prof', 'prof2'})
        self.assertNotIn('email', resp.json()[0])

    def test_search_by_name_returns_cabin(self):
        resp = self.as_user(self.student).get('/api/professors/?search=lovelace')
        self.assertEqual([(p['username'], p['cabin_number']) for p in resp.json()], [('prof', 'A-105')])

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

    def test_cannot_double_book_a_slot(self):
        self.book(student=self.other_student)
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
        self.assertContains(resp, '<option value="professor" selected>', status_code=401)

    def test_user_without_role_is_not_logged_in(self):
        make_user('nobody', '')
        resp = self.login('nobody')
        self.assertContains(resp, 'Admins sign in through the admin site', status_code=403)
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
        for field in ('role', 'cabin_number', 'availability_status', 'first_name'):
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
                'cabin_number': 'B-210',
                'availability_status': 'Busy',
            },
        )
        self.assertEqual(resp.status_code, 302, resp.content[:500])
        prof = CustomUser.objects.get(username='newprof')
        self.assertEqual((prof.role, prof.cabin_number, prof.availability_status), ('professor', 'B-210', 'Busy'))
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

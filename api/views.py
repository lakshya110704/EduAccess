import re
from urllib.parse import quote

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .forms import CabinForm, SignupForm
from .models import (
    AcademicBlock,
    Appointment,
    CustomUser,
    FacultyBlock,
    MyProfessor,
    Notification,
    OpenTime,
    format_cabin,
)
from .permissions import IsAppointmentParticipant, ProfessorHasCabin, dashboard_for, role_required
from .serializers import (
    AppointmentSerializer,
    AppointmentUpdateSerializer,
    MeSerializer,
    NotificationSerializer,
    OpenTimeSerializer,
    ProfessorSerializer,
)


def _name(user):
    return user.get_full_name() or user.username


def _reason(appt):
    return f'{appt.topic} – {appt.details}' if appt.details else appt.topic


def _when(appt):
    start, end = timezone.localtime(appt.appointment_time), timezone.localtime(appt.end_time)
    return f'{start:%d %b %Y, %H:%M}–{end:%H:%M}'


class AppointmentViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """Students book; professors confirm or cancel; students can cancel their own.
    Appointments are never deleted, only cancelled."""

    permission_classes = [IsAuthenticated, ProfessorHasCabin, IsAppointmentParticipant]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['appointment_time']
    http_method_names = ['get', 'post', 'patch', 'head', 'options']

    def get_queryset(self):
        user = self.request.user
        qs = Appointment.objects.select_related('student', 'professor').order_by('appointment_time')
        if user.is_staff:
            return qs
        if user.role == 'professor':
            return qs.filter(professor=user)
        if user.role == 'student':
            return qs.filter(student=user)
        return qs.none()

    def get_serializer_class(self):
        if self.action in ('update', 'partial_update'):
            return AppointmentUpdateSerializer
        return AppointmentSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'student':
            raise PermissionDenied('Only students can book appointments.')
        appt = serializer.save(student=user)
        Notification.objects.create(
            user=appt.professor,
            message=f'New appointment request from {_name(user)} for {_when(appt)}: {_reason(appt)}',
        )

    def perform_update(self, serializer):
        actor = self.request.user
        status_changed = 'status' in serializer.validated_data
        try:
            with transaction.atomic():
                appt = serializer.save()
                if not status_changed:
                    Notification.objects.create(
                        user=appt.professor,
                        message=f'{_name(actor)} updated their request for {_when(appt)}: {_reason(appt)}',
                    )
                    return
                if appt.status == 'Confirmed':
                    self._decline_overlapping_requests(appt)
                recipient = appt.professor if actor == appt.student else appt.student
                Notification.objects.create(
                    user=recipient,
                    message=f'Your appointment with {_name(actor)} on {_when(appt)} is now {appt.status}.',
                )
        except IntegrityError as exc:
            # The Postgres exclusion constraint refused a second overlapping confirmation, e.g. two
            # near-simultaneous "Confirm" clicks that both passed the serializer check.
            raise ValidationError({'status': ['This overlaps another confirmed appointment.']}) from exc

    @staticmethod
    def _decline_overlapping_requests(appt):
        others = Appointment.overlapping(appt.professor, appt.appointment_time, appt.end_time).filter(status='Pending')
        for other in others.exclude(pk=appt.pk).select_related('student'):
            other.status = 'Cancelled'
            other.save(update_fields=['status'])
            Notification.objects.create(
                user=other.student,
                message=f'The slot {_when(other)} with {_name(appt.professor)} was taken. Please pick another slot.',
            )

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        response = super().update(request, *args, **kwargs)
        response.data = AppointmentSerializer(self.get_object(), context=self.get_serializer_context()).data
        return response


class OpenTimeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """A professor's walk-in windows for today. Students see them via `open_today` on /api/professors/."""

    serializer_class = OpenTimeSerializer

    def check_permissions(self, request):
        super().check_permissions(request)
        if request.user.role != 'professor':
            raise PermissionDenied('Only professors set open time.')

    def get_queryset(self):
        return OpenTime.objects.filter(professor=self.request.user, start__date=timezone.localdate())

    @transaction.atomic
    def perform_create(self, serializer):
        window = serializer.save(professor=self.request.user)
        # No appointments inside walk-in time: pending requests it covers are declined.
        covered = Appointment.overlapping(window.professor, window.start, window.end).filter(status='Pending')
        for appt in covered.select_related('student'):
            appt.status = 'Cancelled'
            appt.save(update_fields=['status'])
            start, end = timezone.localtime(window.start), timezone.localtime(window.end)
            Notification.objects.create(
                user=appt.student,
                message=(
                    f'{_name(window.professor)} is in their cabin for walk-ins {start:%H:%M}–{end:%H:%M}, '
                    f'so your request for {_when(appt)} was declined. Just drop by, or pick another slot.'
                ),
            )


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-sent_at')


SEARCH_MIN_CHARS = 2
BLOCK_TOKEN = re.compile(r'^(FB|AB)(\d+)$', re.IGNORECASE)


def professor_search(query):
    """Every word must match. 'FB3' / 'AB2' match the faculty / academic block exactly; other words match
    name, username, cabin or employee ID. So 'AB2 FB3 : 106', 'AB2' and 'gupta' all work."""
    condition = Q()
    for word in query.replace(':', ' ').split():
        block = BLOCK_TOKEN.match(word)
        if block:
            field = 'faculty_block' if block.group(1).upper() == 'FB' else 'academic_block'
            condition &= Q(**{field: int(block.group(2))})
            continue
        text = Q()
        for field in ('username', 'first_name', 'middle_name', 'last_name', 'cabin', 'college_id'):
            text |= Q(**{f'{field}__icontains': word})
        condition &= text
    return condition


SEARCH_MAX_RESULTS = 20


class ProfessorViewSet(viewsets.ReadOnlyModelViewSet):
    """Professors for the student dashboard.

    - `GET /api/professors/` → the requesting student's "My professors" list (what the dashboard polls).
    - `GET /api/professors/?search=…` → search across all professors (>= 2 chars, top 20 matches).
    - `POST` / `DELETE /api/professors/<id>/mine/` → add to / remove from "My professors" (students only).
    """

    serializer_class = ProfessorSerializer

    def all_professors(self):
        return CustomUser.objects.filter(role='professor', is_active=True)

    def my_ids(self):
        return set(MyProfessor.objects.filter(student=self.request.user).values_list('professor_id', flat=True))

    def get_queryset(self):
        return self.all_professors().filter(followed_by_links__student=self.request.user)

    def get_serializer_context(self):
        return {**super().get_serializer_context(), 'my_ids': self.my_ids()}

    def list(self, request, *args, **kwargs):
        query = request.query_params.get('search')
        if query is None:
            professors = self.get_queryset().order_by('first_name', 'last_name', 'username')
        else:
            query = query.strip()
            if len(query) < SEARCH_MIN_CHARS:
                return Response({'detail': f'Type at least {SEARCH_MIN_CHARS} characters to search.'}, status=400)
            professors = (
                self.all_professors()
                .filter(professor_search(query))
                .order_by('first_name', 'last_name')[:SEARCH_MAX_RESULTS]
            )
        return Response(self.get_serializer(professors, many=True).data)

    @action(detail=True, methods=['post', 'delete'], url_path='mine')
    def mine(self, request, pk=None):
        if request.user.role != 'student':
            raise PermissionDenied('Only students have a "My professors" list.')
        professor = get_object_or_404(self.all_professors(), pk=pk)
        if request.method == 'POST':
            MyProfessor.objects.get_or_create(student=request.user, professor=professor)
        else:
            MyProfessor.objects.filter(student=request.user, professor=professor).delete()
        return Response(self.get_serializer(professor).data)


class MeView(generics.RetrieveUpdateAPIView):
    """GET or PATCH the logged-in user (professors set their availability here)."""

    serializer_class = MeSerializer
    http_method_names = ['get', 'patch', 'head', 'options']

    def get_object(self):
        return self.request.user


# Page views


LOGIN_ROLES = {'student': 'Student', 'professor': 'Professor'}


def _wrong_role_message(user):
    if user.role in LOGIN_ROLES:
        return f'This is a {LOGIN_ROLES[user.role].lower()} account. Is the role selected right?'
    return 'This account cannot sign in here.'


def login_view(request):
    """Log in as the selected role: the username and password must belong to an account of that role.
    Honors a `next` parameter when it is a safe local URL."""
    next_url = request.POST.get('next') or request.GET.get('next') or ''
    safe_next = (
        next_url
        if url_has_allowed_host_and_scheme(
            next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
        )
        else ''
    )

    if request.user.is_authenticated and request.method == 'GET':
        target = dashboard_for(request.user)
        if target:
            return redirect(target)

    if request.method == 'POST':
        role = request.POST.get('role', '')
        context = {'next': safe_next, 'selected_role': role}

        def fail(message, status):
            messages.error(request, message)
            return render(request, 'login.html', context, status=status)

        if role not in LOGIN_ROLES:
            return fail('Select your role.', 400)

        username, password = request.POST.get('username'), request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            # authenticate() rejects inactive accounts outright. Only someone who knows the password
            # gets a specific message (role or approval); everyone else gets the same neutral one.
            pending = CustomUser.objects.filter(username=username, is_active=False).first()
            if pending and password and pending.check_password(password):
                if pending.role != role:
                    return fail(_wrong_role_message(pending), 403)
                return fail('Your account is awaiting approval by an admin.', 403)
            return fail(
                'Invalid username or password for the selected role. Check that the right role is selected.', 401
            )

        if user.role != role:
            return fail(_wrong_role_message(user), 403)

        login(request, user)
        return redirect(safe_next or dashboard_for(user))

    return render(request, 'login.html', {'next': safe_next})


def signup_view(request):
    """Self-registration for students and professors. New accounts are inactive until an admin
    activates them in the admin site."""
    if request.user.is_authenticated:
        return redirect(dashboard_for(request.user) or 'login')
    form = SignupForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('signup_done')
    return render(request, 'signup.html', {'form': form, 'email_domains': settings.SIGNUP_EMAIL_DOMAINS})


def go_view(request, academic, faculty, cabin):
    """Directions to a cabin: Google Maps to the academic block, then the faculty block's written directions.
    Shows only the location (no professor names) and needs no login, so it can be opened from a shared link."""
    block = AcademicBlock.objects.filter(number=academic).first()
    faculty_block = FacultyBlock.objects.filter(academic_block=block, number=faculty).first() if block else None
    label = format_cabin(academic, faculty, cabin)
    share_text = f'Directions to cabin {label}: {request.build_absolute_uri()}'
    return render(
        request,
        'go.html',
        {
            'label': label,
            'academic': academic,
            'cabin': cabin,
            'block': block,
            'faculty_block': faculty_block,
            'whatsapp_url': f'https://wa.me/?text={quote(share_text)}',
        },
    )


def signup_done(request):
    return render(request, 'signup-done.html')


@require_POST
def logout_view(request):
    logout(request)
    return redirect('login')


@role_required('student')
def student_dashboard(request):
    return render(
        request,
        'student-dashboard.html',
        {'topics': Appointment.TOPIC_CHOICES, 'details_max': Appointment.DETAILS_MAX_LENGTH},
    )


@role_required('professor')
def professor_dashboard(request):
    if not request.user.has_cabin:
        return redirect('professor_cabin')
    return render(request, 'professor-dashboard.html', {'cabin_form': _cabin_form(request.user)})


def _cabin_form(user, data=None):
    initial = {'cabin': user.cabin}
    faculty = FacultyBlock.objects.filter(academic_block__number=user.academic_block, number=user.faculty_block).first()
    if faculty:
        initial.update(academic_block=faculty.academic_block_id, faculty_block=faculty.id)
    return CabinForm(data, initial=initial)


@role_required('professor')
def professor_cabin(request):
    """Set or change the cabin. Professors without one are sent here and can't use the dashboard until they save."""
    form = _cabin_form(request.user, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save(request.user)
        messages.success(request, f'Cabin saved: {request.user.cabin_label}.')
        return redirect('professor_dashboard')
    return render(request, 'professor-cabin.html', {'cabin_form': form, 'first_time': not request.user.has_cabin})

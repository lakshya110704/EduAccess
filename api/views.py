from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, mixins, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from .forms import SignupForm
from .models import Appointment, CustomUser, Notification
from .permissions import IsAppointmentParticipant, dashboard_for, role_required
from .serializers import (
    AppointmentSerializer,
    AppointmentStatusSerializer,
    MeSerializer,
    NotificationSerializer,
    ProfessorSerializer,
)


def _name(user):
    return user.get_full_name() or user.username


class AppointmentViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """Students book; professors confirm or cancel; students can cancel their own.
    Appointments are never deleted, only cancelled."""

    permission_classes = [IsAuthenticated, IsAppointmentParticipant]
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
            return AppointmentStatusSerializer
        return AppointmentSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'student':
            raise PermissionDenied('Only students can book appointments.')
        appt = serializer.save(student=user)
        Notification.objects.create(
            user=appt.professor,
            message=f'New appointment request from {_name(user)} for {appt.appointment_time:%d %b %Y, %H:%M}.',
        )

    @transaction.atomic
    def perform_update(self, serializer):
        appt = serializer.save()
        actor = self.request.user
        recipient = appt.professor if actor == appt.student else appt.student
        Notification.objects.create(
            user=recipient,
            message=(
                f'Your appointment with {_name(actor)} on {appt.appointment_time:%d %b %Y, %H:%M} is now {appt.status}.'
            ),
        )

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        response = super().update(request, *args, **kwargs)
        response.data = AppointmentSerializer(self.get_object(), context=self.get_serializer_context()).data
        return response


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-sent_at')


class ProfessorViewSet(viewsets.ReadOnlyModelViewSet):
    """Directory of professors: availability and cabin. Searchable by name."""

    serializer_class = ProfessorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'first_name', 'last_name', 'cabin_number']

    def get_queryset(self):
        return CustomUser.objects.filter(role='professor', is_active=True).order_by('first_name', 'username')


class MeView(generics.RetrieveUpdateAPIView):
    """GET or PATCH the logged-in user (professors set their availability here)."""

    serializer_class = MeSerializer
    http_method_names = ['get', 'patch', 'head', 'options']

    def get_object(self):
        return self.request.user


# Page views


def login_view(request):
    """Authenticate and send the user to the dashboard for their stored role.
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
        username, password = request.POST.get('username'), request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            # authenticate() rejects inactive accounts outright; tell a signed-up user (who knows their
            # password) that they are waiting for approval rather than that the password is wrong.
            pending = CustomUser.objects.filter(username=username, is_active=False).first()
            if pending and password and pending.check_password(password):
                messages.error(request, 'Your account is awaiting approval by an admin.')
                return render(request, 'login.html', {'next': safe_next}, status=403)
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html', {'next': safe_next}, status=401)

        target = dashboard_for(user)
        if target is None:
            messages.error(request, 'Your account does not have a role yet. Please contact an admin.')
            return render(request, 'login.html', {'next': safe_next}, status=403)

        login(request, user)
        return redirect(safe_next or target)

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


def signup_done(request):
    return render(request, 'signup-done.html')


@require_POST
def logout_view(request):
    logout(request)
    return redirect('login')


@role_required('student')
def student_dashboard(request):
    return render(request, 'student-dashboard.html')


@role_required('professor')
def professor_dashboard(request):
    return render(request, 'professor-dashboard.html')

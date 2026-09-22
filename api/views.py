from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Appointment, Notification, CustomUser
from .serializers import AppointmentSerializer, NotificationSerializer, CustomUserSerializer
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]  # Login required
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['appointment_time']

    def get_queryset(self):
        user = self.request.user

        if user.role == 'professor':
            return Appointment.objects.filter(professor=user).order_by('appointment_time')

        elif user.role == 'student':
            return Appointment.objects.filter(student=user).order_by('appointment_time')

        return Appointment.objects.all().order_by('appointment_time')

    def perform_create(self, serializer):
        user = self.request.user

        if user.role != 'student':
            raise PermissionDenied("Only students can create appointments.")

        # Auto-fill student; professor must still be selected in frontend
        serializer.save(student=user)

    def perform_update(self, serializer):
        instance = serializer.save()

        if 'status' in serializer.validated_data:
            Notification.objects.create(
                user=instance.student,
                message=f"Your appointment with {instance.professor.username} is now {instance.status}."
            )

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Notification.objects.none()
        return Notification.objects.filter(user=user).order_by('-sent_at')

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.filter(role__iexact='professor')

from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings


def login_view(request):
    """Authenticate user and redirect to the correct dashboard.
    Falls back to the user's stored role if no role is selected in the form.
    Also respects an optional `next` parameter when it's a safe local URL.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        selected_role = (request.POST.get('role') or '').strip().lower()

        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, 'Invalid username or password.')
            return redirect('/login/')

        # Successful auth: log the user in
        login(request, user)

        # If a safe `next` URL is provided, honor it first
        next_url = request.POST.get('next') or request.GET.get('next')
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
            return redirect(next_url)

        # Determine effective role: prefer explicit selection, else user's stored role
        user_role = (getattr(user, 'role', '') or '').strip().lower()
        effective_role = selected_role or user_role

        # Redirect by role
        if effective_role == 'student':
            return redirect('/student/')
        if effective_role == 'professor':
            return redirect('/professor/')
        if effective_role == 'admin' or getattr(user, 'is_superuser', False):
            return redirect('/admin/')

        # If we reach here, we couldn't resolve a role cleanly
        messages.error(request, 'Your account does not have a recognized role. Please contact an admin.')
        return redirect('/login/')

    # GET request → render login page
    return render(request, 'login.html')

@login_required
def current_user_id_view(request):
    return JsonResponse({'id': request.user.id})

@login_required
def student_dashboard(request):
    professors = CustomUser.objects.filter(role__iexact='professor')
    return render(request, 'student-dashboard.html', {'professors': professors})


@login_required
def professor_dashboard(request):
    return render(request, 'professor-dashboard.html')


@login_required
def get_professors_data(request):
    professors = CustomUser.objects.filter(role='professor')
    data = [{'username': prof.username, 'availability': prof.availability_status} for prof in professors]
    return JsonResponse({'professors': data})
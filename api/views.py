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

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            user_role = user.role.lower() if user.role else ''
            selected_role = role.lower() if role else ''

            if selected_role == 'student' and user_role == 'student':
                return redirect('/student/')
            elif selected_role == 'professor' and user_role == 'professor':
                return redirect('/professor/')
            elif selected_role == 'admin' and user.is_superuser:
                return redirect('/admin/')
            else:
                messages.error(request, 'Selected role does not match your profile.')
                return redirect('/login/')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('/login/')
    else:
        return render(request, 'login.html')

@login_required
def current_user_id_view(request):
    return JsonResponse({'id': request.user.id})

@login_required
def student_dashboard(request):
    professors = CustomUser.objects.filter(role__iexact='professor')
    return render(request, 'student-dashboard.html', {'professors': professors})

from django.http import JsonResponse
from .models import CustomUser

@login_required
def get_professors_data(request):
    professors = CustomUser.objects.filter(role='professor')
    data = [{'username': prof.username, 'availability': prof.availability_status} for prof in professors]
    return JsonResponse({'professors': data})
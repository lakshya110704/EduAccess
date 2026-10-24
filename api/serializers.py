from django.utils import timezone
from rest_framework import serializers

from .models import Appointment, CustomUser, Notification


class ProfessorSerializer(serializers.ModelSerializer):
    """Public, read-only view of a professor for students."""

    display_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'display_name', 'availability_status', 'cabin_number']
        read_only_fields = fields

    def get_display_name(self, obj):
        return obj.get_full_name() or obj.username


class MeSerializer(serializers.ModelSerializer):
    """The logged-in user. Only availability is editable, and only by professors."""

    display_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'display_name', 'role', 'availability_status', 'cabin_number']
        read_only_fields = ['id', 'username', 'display_name', 'role', 'cabin_number']

    def get_display_name(self, obj):
        return obj.get_full_name() or obj.username

    def validate(self, attrs):
        if 'availability_status' in attrs and self.instance.role != 'professor':
            raise serializers.ValidationError('Only professors have an availability status.')
        return attrs


class AppointmentSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    professor_name = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ['id', 'student', 'student_name', 'professor', 'professor_name', 'appointment_time', 'status']
        read_only_fields = ['id', 'student', 'status']

    def get_student_name(self, obj):
        return obj.student.get_full_name() or obj.student.username

    def get_professor_name(self, obj):
        return obj.professor.get_full_name() or obj.professor.username

    def validate_professor(self, value):
        if value.role != 'professor' or not value.is_active:
            raise serializers.ValidationError('Select a valid professor.')
        return value

    def validate_appointment_time(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError('Appointment time must be in the future.')
        return value

    def validate(self, attrs):
        professor = attrs.get('professor')
        when = attrs.get('appointment_time')
        if professor and when:
            clash = Appointment.objects.filter(
                professor=professor,
                appointment_time=when,
                status__in=['Pending', 'Confirmed'],
            ).exists()
            if clash:
                raise serializers.ValidationError('That slot is already booked. Pick another time.')
        return attrs


class AppointmentStatusSerializer(serializers.ModelSerializer):
    """Used for updates: the only thing that can change after booking is the status."""

    class Meta:
        model = Appointment
        fields = ['status']

    def validate_status(self, value):
        user = self.context['request'].user
        appt = self.instance
        if appt.status == 'Cancelled':
            raise serializers.ValidationError('This appointment is already cancelled.')
        if user == appt.professor:
            allowed = {'Confirmed', 'Cancelled'}
        elif user == appt.student:
            allowed = {'Cancelled'}
        else:
            allowed = set()
        if value not in allowed:
            raise serializers.ValidationError(f'You cannot set this appointment to {value}.')
        return value


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'sent_at']
        read_only_fields = fields

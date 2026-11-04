from django.utils import timezone
from rest_framework import serializers

from .models import SLOT_LENGTH, Appointment, CustomUser, Notification, OpenTime


class ProfessorSerializer(serializers.ModelSerializer):
    """Public, read-only view of a professor for students. `is_mine` needs `my_ids` in the context."""

    display_name = serializers.SerializerMethodField()
    is_mine = serializers.SerializerMethodField()
    open_today = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'display_name',
            'availability_status',
            'cabin_label',
            'directions_url',
            'is_mine',
            'open_today',
        ]
        read_only_fields = fields

    def get_open_today(self, obj):
        windows = OpenTime.objects.filter(professor=obj, start__date=timezone.localdate()).order_by('start')
        return [{'start': w.start, 'end': w.end} for w in windows]

    directions_url = serializers.CharField(source='directions_path', read_only=True)

    def get_display_name(self, obj):
        return obj.get_full_name() or obj.username

    def get_is_mine(self, obj):
        return obj.id in self.context.get('my_ids', set())


class MeSerializer(serializers.ModelSerializer):
    """The logged-in user. Only availability is editable, and only by professors."""

    display_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'display_name', 'role', 'availability_status', 'cabin_label']
        read_only_fields = ['id', 'username', 'display_name', 'role', 'cabin_label']

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
        fields = [
            'id',
            'student',
            'student_name',
            'professor',
            'professor_name',
            'appointment_time',
            'slots',
            'end_time',
            'status',
            'topic',
            'details',
        ]
        read_only_fields = ['id', 'student', 'end_time', 'status']
        extra_kwargs = {'topic': {'required': True}}

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
        local = timezone.localtime(value)
        if local.minute % 15 or local.second or local.microsecond:
            raise serializers.ValidationError('Appointments start on the quarter hour (:00, :15, :30 or :45).')
        return value

    def validate(self, attrs):
        # Overlapping *pending* requests are allowed: the professor picks one, and accepting it declines
        # the others. Only time that is already taken (a confirmed appointment) is refused here.
        professor = attrs.get('professor')
        start = attrs.get('appointment_time')
        if professor and start:
            end = start + attrs.get('slots', 1) * SLOT_LENGTH
            if Appointment.overlapping(professor, start, end).filter(status='Confirmed').exists():
                raise serializers.ValidationError('That time is already booked. Pick another slot.')
            if OpenTime.overlapping(professor, start, end).exists():
                raise serializers.ValidationError('That is open (walk-in) time: no appointment needed, just drop by.')
        return attrs


def _check_quarter_hour(value, label):
    local = timezone.localtime(value)
    if local.minute % 15 or local.second or local.microsecond:
        raise serializers.ValidationError(f'{label} must be on the quarter hour (:00, :15, :30 or :45).')


class OpenTimeSerializer(serializers.ModelSerializer):
    """A professor's walk-in window for today. Can't overlap their confirmed appointments."""

    class Meta:
        model = OpenTime
        fields = ['id', 'start', 'end']

    def validate(self, attrs):
        start, end = attrs['start'], attrs['end']
        _check_quarter_hour(start, 'Start')
        _check_quarter_hour(end, 'End')
        if end <= start:
            raise serializers.ValidationError('End must be after start.')
        if timezone.localdate(start) != timezone.localdate() or timezone.localdate(end) != timezone.localdate():
            raise serializers.ValidationError('Open time is set for today only.')
        professor = self.context['request'].user
        if OpenTime.overlapping(professor, start, end).exists():
            raise serializers.ValidationError('This overlaps open time you already set.')
        if Appointment.overlapping(professor, start, end).filter(status='Confirmed').exists():
            raise serializers.ValidationError('You have a confirmed appointment in that time.')
        return attrs


class AppointmentUpdateSerializer(serializers.ModelSerializer):
    """Used for updates: the status, and the student's reason while the request is still pending."""

    class Meta:
        model = Appointment
        fields = ['status', 'topic', 'details']

    def validate(self, attrs):
        if 'topic' in attrs or 'details' in attrs:
            appt = self.instance
            if self.context['request'].user != appt.student:
                raise serializers.ValidationError('Only the student who booked can change the reason.')
            if appt.status != 'Pending':
                raise serializers.ValidationError('The reason can only be changed while the request is pending.')
        return attrs

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
        if value == 'Confirmed':
            taken = Appointment.overlapping(appt.professor, appt.appointment_time, appt.end_time)
            if taken.filter(status='Confirmed').exclude(pk=appt.pk).exists():
                raise serializers.ValidationError('This overlaps another confirmed appointment.')
        return value


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'sent_at']
        read_only_fields = fields

import re
from datetime import timedelta

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.db.models import Q
from django.db.models.functions import Lower

# Role options
USER_ROLES = (
    ('student', 'Student'),
    ('professor', 'Professor'),
    ('admin', 'Admin'),
)

# Appointments are booked in 15-minute slots; a request covers one or two consecutive slots.
SLOT_LENGTH = timedelta(minutes=15)
SLOT_CHOICES = ((1, '15 minutes'), (2, '30 minutes (2 slots)'))

# Cabin locations are written "FB3 AB2 : 106": Faculty Block 3 inside Academic Block 2, cabin 106.
CABIN_PATTERN = re.compile(r'^\s*FB\s*(\d+)\s*AB\s*(\d+)\s*:?\s*(\S+)\s*$', re.IGNORECASE)


def parse_cabin(text):
    """'FB3 AB2 : 106' -> (academic_block=2, faculty_block=3, cabin='106'), or None if it isn't in that format."""
    match = CABIN_PATTERN.match(text or '')
    if not match:
        return None
    faculty_block, academic_block, cabin = match.groups()
    return int(academic_block), int(faculty_block), cabin.upper()


def format_cabin(academic_block, faculty_block, cabin):
    if academic_block and faculty_block and cabin:
        return f'FB{faculty_block} AB{academic_block} : {cabin}'
    return cabin or ''


# Availability options
AVAILABILITY_CHOICES = (
    ('Free', 'Free'),
    ('Busy', 'Busy'),
    ('Unavailable', 'Unavailable'),
)


class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=USER_ROLES)
    availability_status = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='Unavailable')
    # Cabin location, displayed as "FB<faculty_block> AB<academic_block> : <cabin>".
    academic_block = models.PositiveSmallIntegerField(null=True, blank=True)
    faculty_block = models.PositiveSmallIntegerField(null=True, blank=True)
    cabin = models.CharField('cabin number', max_length=10, blank=True, default='')
    middle_name = models.CharField(max_length=150, blank=True, default='')
    # Roll number for students, employee ID for professors.
    college_id = models.CharField('college ID', max_length=30, blank=True, default='')

    # Fix reverse accessor conflict errors in admin logs
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    class Meta(AbstractUser.Meta):
        constraints = [
            # One account per email (case-insensitive); accounts without an email are exempt.
            models.UniqueConstraint(Lower('email'), condition=~Q(email=''), name='unique_email_ci'),
            # A roll number / employee ID identifies one person within a role.
            models.UniqueConstraint(
                fields=['role', 'college_id'], condition=~Q(college_id=''), name='unique_college_id_per_role'
            ),
        ]

    def __str__(self):
        return f'{self.username} ({self.role})'

    @property
    def cabin_label(self):
        return format_cabin(self.academic_block, self.faculty_block, self.cabin)

    @property
    def directions_path(self):
        """Path of the cabin directions page, or '' if the cabin location is incomplete."""
        if self.academic_block and self.faculty_block and self.cabin:
            return f'/go/AB{self.academic_block}/FB{self.faculty_block}/{self.cabin}/'
        return ''

    def get_full_name(self):
        return ' '.join(part for part in (self.first_name, self.middle_name, self.last_name) if part).strip()


class Appointment(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    )

    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appointments_made')
    professor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appointments_received')
    appointment_time = models.DateTimeField()
    slots = models.PositiveSmallIntegerField(choices=SLOT_CHOICES, default=1)
    # Stored (not computed in SQL) so the Postgres exclusion constraint can index tstzrange(start, end):
    # "start + interval" isn't IMMUTABLE in Postgres and can't be used in a constraint.
    end_time = models.DateTimeField(editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f'{self.student.username} → {self.professor.username} @ {self.appointment_time} ({self.status})'

    def save(self, *args, **kwargs):
        self.end_time = self.appointment_time + self.slots * SLOT_LENGTH
        super().save(*args, **kwargs)

    @classmethod
    def overlapping(cls, professor, start, end):
        """Appointments of `professor` whose [start, end) range overlaps the given one."""
        return cls.objects.filter(professor=professor, appointment_time__lt=end, end_time__gt=start)


class AcademicBlock(models.Model):
    """A campus building (AB1, AB2, ...). Its entrance coordinates drive the outdoor Google Maps directions."""

    number = models.PositiveSmallIntegerField(unique=True)
    name = models.CharField(max_length=100, blank=True, help_text='Optional, e.g. "Academic Block 2".')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    view_360_url = models.URLField(
        '360° view link', blank=True, help_text='Virtual tour or Street View of the entrance.'
    )

    class Meta:
        ordering = ['number']

    def __str__(self):
        return self.name or f'Academic Block {self.number}'

    @property
    def maps_url(self):
        if self.latitude is None or self.longitude is None:
            return ''
        return f'https://www.google.com/maps/dir/?api=1&destination={self.latitude},{self.longitude}&travelmode=walking'


class FacultyBlock(models.Model):
    """A faculty block inside an academic block. A faculty block is on a single floor."""

    academic_block = models.ForeignKey(AcademicBlock, on_delete=models.CASCADE, related_name='faculty_blocks')
    number = models.PositiveSmallIntegerField()
    floor = models.SmallIntegerField(help_text='0 = ground floor.')
    directions = models.TextField(help_text='How to get here from the academic block entrance or lobby.')

    class Meta:
        ordering = ['academic_block__number', 'number']
        constraints = [models.UniqueConstraint(fields=['academic_block', 'number'], name='unique_faculty_block')]

    def __str__(self):
        return f'FB{self.number} AB{self.academic_block.number}'

    @property
    def floor_label(self):
        return 'Ground floor' if self.floor == 0 else f'Floor {self.floor}'


class OpenTime(models.Model):
    """A window when a professor is in their cabin and anyone may walk in. No appointments inside it."""

    professor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='open_times')
    start = models.DateTimeField()
    end = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start']
        constraints = [
            models.CheckConstraint(condition=models.Q(end__gt=models.F('start')), name='open_time_end_after_start')
        ]

    def __str__(self):
        return f'{self.professor.username} open {self.start:%Y-%m-%d %H:%M}–{self.end:%H:%M}'

    @classmethod
    def overlapping(cls, professor, start, end):
        return cls.objects.filter(professor=professor, start__lt=end, end__gt=start)


class MyProfessor(models.Model):
    """A professor a student has added to their "My professors" list."""

    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='my_professor_links')
    professor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='followed_by_links')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['student', 'professor'], name='unique_my_professor')]

    def __str__(self):
        return f'{self.student.username} ☆ {self.professor.username}'


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'To: {self.user.username} → {self.message[:40]}'

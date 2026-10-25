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

# Availability options
AVAILABILITY_CHOICES = (
    ('Free', 'Free'),
    ('Busy', 'Busy'),
    ('Unavailable', 'Unavailable'),
)


class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=USER_ROLES)
    availability_status = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='Unavailable')
    cabin_number = models.CharField(max_length=10, blank=True, default='')
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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f'{self.student.username} → {self.professor.username} @ {self.appointment_time} ({self.status})'


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'To: {self.user.username} → {self.message[:40]}'

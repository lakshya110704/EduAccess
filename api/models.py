from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

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
    cabin_number = models.CharField(max_length=10, blank=True, null=True)

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

    def __str__(self):
        return f"{self.username} ({self.role})"
    

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
        return f"{self.student.username} → {self.professor.username} @ {self.appointment_time} ({self.status})"
    
class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To: {self.user.username} → {self.message[:40]}"
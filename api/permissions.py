from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from rest_framework import permissions


def dashboard_for(user):
    """URL of the dashboard a user should land on, or None if they have no usable role."""
    if user.role == 'student':
        return '/student/'
    if user.role == 'professor':
        return '/professor/'
    if user.is_staff:
        return '/admin/'
    return None


def role_required(role):
    """Page view decorator: require login and the given role."""

    def decorator(view):
        @wraps(view)
        @login_required
        def wrapped(request, *args, **kwargs):
            if request.user.role != role:
                raise PermissionDenied
            return view(request, *args, **kwargs)

        return wrapped

    return decorator


class IsAppointmentParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_staff or obj.student_id == user.id or obj.professor_id == user.id

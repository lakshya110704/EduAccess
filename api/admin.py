from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Appointment, CustomUser, Notification


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'first_name', 'last_name', 'role', 'availability_status', 'cabin_number', 'is_active']
    list_filter = ('role', *UserAdmin.list_filter)

    # "Add user" page: account and EduAccess profile on one page, so a student or professor
    # is fully set up with a single save.
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'EduAccess profile',
            {
                'classes': ('wide',),
                'fields': ('first_name', 'last_name', 'email', 'role', 'cabin_number', 'availability_status'),
            },
        ),
    )

    # "Change user" page: Django's sections plus the EduAccess fields.
    fieldsets = UserAdmin.fieldsets + (
        (
            'Additional Info',
            {
                'fields': ('role', 'availability_status', 'cabin_number'),
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Appointment)
admin.site.register(Notification)

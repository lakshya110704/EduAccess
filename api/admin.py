from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Appointment, Notification

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'availability_status', 'cabin_number', 'is_active']
    
    # Show custom fields in the admin form
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'availability_status', 'cabin_number'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Appointment)
admin.site.register(Notification)
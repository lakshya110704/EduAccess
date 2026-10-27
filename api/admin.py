from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin

from .models import Appointment, CustomUser, Notification


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'first_name', 'last_name', 'role', 'college_id', 'email', 'cabin_number', 'is_active']
    list_filter = ('role', *UserAdmin.list_filter)
    search_fields = (*UserAdmin.search_fields, 'college_id')
    actions = ['activate_accounts']

    # "Add user" page: account and EduAccess profile on one page, so a student or professor
    # is fully set up with a single save.
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'EduAccess profile',
            {
                'classes': ('wide',),
                'fields': (
                    'first_name',
                    'middle_name',
                    'last_name',
                    'email',
                    'role',
                    'college_id',
                    'cabin_number',
                    'availability_status',
                ),
            },
        ),
    )

    # "Change user" page: Django's sections plus the EduAccess fields.
    fieldsets = UserAdmin.fieldsets + (
        (
            'Additional Info',
            {
                'fields': ('role', 'middle_name', 'college_id', 'availability_status', 'cabin_number'),
            },
        ),
    )

    @admin.action(description='Activate selected accounts')
    def activate_accounts(self, request, queryset):
        updated = queryset.filter(is_active=False).update(is_active=True)
        self.message_user(request, f'Activated {updated} account(s).', messages.SUCCESS)


admin.site.site_header = 'EduAccess Admin'
admin.site.site_title = 'EduAccess Admin'
admin.site.index_title = 'Manage EduAccess'

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Appointment)
admin.site.register(Notification)

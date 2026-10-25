from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser

SIGNUP_ROLES = [('student', 'Student'), ('professor', 'Professor')]
COLLEGE_ID_LABELS = {'student': 'roll number', 'professor': 'employee ID'}


class SignupForm(UserCreationForm):
    """Self-registration. Every rule is enforced here on the server; the page's JavaScript only
    adjusts labels. Accounts are created inactive and must be activated by an admin."""

    role = forms.ChoiceField(choices=SIGNUP_ROLES)
    first_name = forms.CharField(max_length=150)
    middle_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField(label='College email')
    college_id = forms.CharField(max_length=30, label='Roll number / Employee ID')

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('role', 'username', 'first_name', 'middle_name', 'last_name', 'email', 'college_id')

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def clean_college_id(self):
        return self.cleaned_data['college_id'].strip().upper()

    def clean(self):
        cleaned = super().clean()
        role = cleaned.get('role')
        email = cleaned.get('email')
        college_id = cleaned.get('college_id')
        if role and email:
            domain = settings.SIGNUP_EMAIL_DOMAINS[role]
            if email.rsplit('@', 1)[-1] != domain:
                self.add_error('email', f'{role.capitalize()}s must register with their @{domain} email.')
        if role and college_id and CustomUser.objects.filter(role=role, college_id=college_id).exists():
            self.add_error('college_id', f'An account with this {COLLEGE_ID_LABELS[role]} already exists.')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        if commit:
            user.save()
        return user

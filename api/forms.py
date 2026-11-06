import re

from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm

from .models import AcademicBlock, CustomUser, FacultyBlock

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


CABIN_NUMBER = re.compile(r'^[A-Z0-9-]{1,10}$')
# Only academic blocks a professor can actually finish choosing from.
CABIN_ACADEMIC_BLOCKS = AcademicBlock.objects.filter(faculty_blocks__isnull=False).distinct()


class CabinForm(forms.Form):
    """A professor's cabin location, picked from the blocks set up in the admin so directions always work.
    The page's JavaScript only filters the faculty block list to the chosen academic block."""

    academic_block = forms.ModelChoiceField(
        queryset=CABIN_ACADEMIC_BLOCKS,
        empty_label='Academic block',
    )
    faculty_block = forms.ModelChoiceField(
        queryset=FacultyBlock.objects.select_related('academic_block'), empty_label='Faculty block'
    )
    cabin = forms.CharField(max_length=10, label='Cabin number')

    def clean_cabin(self):
        cabin = self.cleaned_data['cabin'].strip().upper()
        if not CABIN_NUMBER.match(cabin):
            raise forms.ValidationError('Use letters, digits and dashes only, e.g. 106 or G-12.')
        return cabin

    def clean(self):
        cleaned = super().clean()
        academic, faculty = cleaned.get('academic_block'), cleaned.get('faculty_block')
        if academic and faculty and faculty.academic_block_id != academic.id:
            self.add_error('faculty_block', f'That faculty block is not in {academic}.')
        return cleaned

    def save(self, user):
        user.academic_block = self.cleaned_data['academic_block'].number
        user.faculty_block = self.cleaned_data['faculty_block'].number
        user.cabin = self.cleaned_data['cabin']
        user.save(update_fields=['academic_block', 'faculty_block', 'cabin'])

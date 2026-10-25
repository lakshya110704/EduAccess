from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from api.models import CustomUser

DEMO_PASSWORD = 'eduaccess-demo-2026'

DEMO_USERS = [
    {'username': 'student1', 'role': 'student', 'first_name': 'Riya', 'last_name': 'Sharma'},
    {'username': 'student2', 'role': 'student', 'first_name': 'Arjun', 'last_name': 'Verma'},
    {
        'username': 'prof1',
        'role': 'professor',
        'first_name': 'Ashish',
        'last_name': 'Gupta',
        'cabin_number': 'A-105',
        'availability_status': 'Free',
    },
    {
        'username': 'prof2',
        'role': 'professor',
        'first_name': 'Neha',
        'last_name': 'Iyer',
        'cabin_number': 'B-210',
        'availability_status': 'Busy',
    },
]


class Command(BaseCommand):
    help = f'Create demo students and professors (password: {DEMO_PASSWORD}). DEBUG only.'

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError('seed_demo only runs with DJANGO_DEBUG=True.')
        for spec in DEMO_USERS:
            spec = dict(spec)
            username = spec.pop('username')
            user, created = CustomUser.objects.update_or_create(username=username, defaults=spec)
            user.set_password(DEMO_PASSWORD)
            user.save()
            self.stdout.write(f'{"created" if created else "updated"} {username} ({user.role})')

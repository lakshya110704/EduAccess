import re

from django.db import migrations, models

CABIN_PATTERN = re.compile(r'^\s*FB\s*(\d+)\s*AB\s*(\d+)\s*:?\s*(\S+)\s*$', re.IGNORECASE)


def split_cabins(apps, schema_editor):
    """Move "FB3 AB2 : 106"-style values into the new fields; report any that don't match."""
    CustomUser = apps.get_model('api', 'CustomUser')
    unparsed = []
    for user in CustomUser.objects.exclude(cabin_number=''):
        match = CABIN_PATTERN.match(user.cabin_number)
        if match:
            faculty_block, academic_block, cabin = match.groups()
            user.academic_block, user.faculty_block, user.cabin = int(academic_block), int(faculty_block), cabin.upper()
            user.save(update_fields=['academic_block', 'faculty_block', 'cabin'])
        else:
            unparsed.append(f'{user.username} ({user.cabin_number!r})')
    if unparsed:
        print(f'\n  Cabins not in "FB<n> AB<n> : <room>" format, re-enter in the admin: {", ".join(unparsed)}')


def join_cabins(apps, schema_editor):
    CustomUser = apps.get_model('api', 'CustomUser')
    for user in CustomUser.objects.exclude(cabin=''):
        if user.academic_block and user.faculty_block:
            user.cabin_number = f'FB{user.faculty_block}AB{user.academic_block}:{user.cabin}'[:10]
        else:
            user.cabin_number = user.cabin
        user.save(update_fields=['cabin_number'])


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0008_open_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='academic_block',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='faculty_block',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='cabin',
            field=models.CharField(blank=True, default='', max_length=10, verbose_name='cabin number'),
        ),
        migrations.RunPython(split_cabins, join_cabins),
        migrations.RemoveField(
            model_name='customuser',
            name='cabin_number',
        ),
    ]

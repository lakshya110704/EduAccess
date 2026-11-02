from datetime import timedelta

from django.db import migrations, models

CONSTRAINT = 'appointment_no_confirmed_overlap'


def fill_end_times(apps, schema_editor):
    Appointment = apps.get_model('api', 'Appointment')
    for appt in Appointment.objects.all():
        appt.end_time = appt.appointment_time + appt.slots * timedelta(minutes=15)
        appt.save(update_fields=['end_time'])


def add_overlap_constraint(apps, schema_editor):
    # PostgreSQL only: no two *confirmed* appointments of one professor may overlap in time. The database
    # enforces this even when two confirmations race. SQLite (local runs/tests) relies on the app checks.
    if schema_editor.connection.vendor != 'postgresql':
        return
    schema_editor.execute('CREATE EXTENSION IF NOT EXISTS btree_gist')
    schema_editor.execute(
        f'ALTER TABLE api_appointment ADD CONSTRAINT {CONSTRAINT} EXCLUDE USING gist ('
        "professor_id WITH =, tstzrange(appointment_time, end_time, '[)') WITH &&"
        ") WHERE (status = 'Confirmed')"
    )


def drop_overlap_constraint(apps, schema_editor):
    if schema_editor.connection.vendor == 'postgresql':
        schema_editor.execute(f'ALTER TABLE api_appointment DROP CONSTRAINT IF EXISTS {CONSTRAINT}')


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0006_my_professors'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='slots',
            field=models.PositiveSmallIntegerField(choices=[(1, '15 minutes'), (2, '30 minutes (2 slots)')], default=1),
        ),
        migrations.AddField(
            model_name='appointment',
            name='end_time',
            field=models.DateTimeField(editable=False, null=True),
        ),
        migrations.RunPython(fill_end_times, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='appointment',
            name='end_time',
            field=models.DateTimeField(editable=False),
        ),
        migrations.RunPython(add_overlap_constraint, drop_overlap_constraint),
    ]

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0011_faculty_block_optional_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='topic',
            field=models.CharField(
                choices=[
                    ('Doubt', 'Doubt'),
                    ('Project', 'Project'),
                    ('Attendance', 'Attendance'),
                    ('Marks', 'Marks'),
                    ('Other', 'Other'),
                ],
                default='Other',  # existing appointments predate the reason field
                max_length=20,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appointment',
            name='details',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]

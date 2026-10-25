from django.db import migrations, models


def null_cabins_to_empty(apps, schema_editor):
    # The column must hold no NULLs before it can become NOT NULL.
    CustomUser = apps.get_model('api', 'CustomUser')
    CustomUser.objects.filter(cabin_number__isnull=True).update(cabin_number='')


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0003_notification'),
    ]

    operations = [
        migrations.RunPython(null_cabins_to_empty, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='customuser',
            name='cabin_number',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
    ]

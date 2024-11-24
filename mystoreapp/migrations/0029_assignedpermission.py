# Generated by Django 4.2.5 on 2023-12-02 20:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mystoreapp', '0028_project_project_serial_no_task_task_serial_no'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignedPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mystoreapp.project')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 4.2.5 on 2023-11-24 10:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mystoreapp', '0016_alter_project_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasksubmission',
            name='image_1',
        ),
        migrations.RemoveField(
            model_name='tasksubmission',
            name='image_2',
        ),
        migrations.RemoveField(
            model_name='tasksubmission',
            name='image_3',
        ),
        migrations.RemoveField(
            model_name='tasksubmission',
            name='image_4',
        ),
        migrations.RemoveField(
            model_name='tasksubmission',
            name='image_5',
        ),
        migrations.RemoveField(
            model_name='tasksubmission',
            name='installation_requirements',
        ),
        migrations.AddField(
            model_name='tasksubmission',
            name='height_measurement',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='tasksubmission',
            name='length_measurement',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='tasksubmission',
            name='status',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='tasksubmission',
            name='submission_feedback',
            field=models.TextField(null=True),
        ),
        migrations.CreateModel(
            name='SubmissionImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission_feedback', models.TextField()),
                ('status', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, upload_to='task_submissions/')),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('task_submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_submissions', to='mystoreapp.tasksubmission')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 4.2.5 on 2023-12-02 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mystoreapp', '0027_remove_submissionimages_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='project_serial_no',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='task_serial_no',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
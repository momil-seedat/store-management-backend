# Generated by Django 4.2.5 on 2024-05-18 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mystoreapp', '0038_project_end_date_project_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(max_length=50),
        ),
    ]
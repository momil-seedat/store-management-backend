# Generated by Django 4.2.5 on 2024-06-22 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mystoreapp', '0039_alter_project_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='progress',
            field=models.CharField(max_length=50, null=True),
        ),
    ]

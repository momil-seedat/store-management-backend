# Generated by Django 4.2.5 on 2023-12-09 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mystoreapp', '0031_rename_assignee_id_assignedpermission_assignee_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignedpermission',
            old_name='use',
            new_name='user',
        ),
    ]
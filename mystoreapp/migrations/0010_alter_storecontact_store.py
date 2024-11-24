# Generated by Django 4.2.5 on 2023-09-23 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mystoreapp', '0009_store_contacts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storecontact',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store', to='mystoreapp.store'),
        ),
    ]

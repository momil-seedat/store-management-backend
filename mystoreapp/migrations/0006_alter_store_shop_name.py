# Generated by Django 4.2.5 on 2023-09-23 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mystoreapp', '0005_storecontact_remove_store_contact_remove_store_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='shop_name',
            field=models.CharField(max_length=255),
        ),
    ]
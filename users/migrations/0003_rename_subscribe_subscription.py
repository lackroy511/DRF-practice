# Generated by Django 4.2.3 on 2023-08-12 04:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_delete_subscribe'),
        ('users', '0002_subscribe'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Subscribe',
            new_name='Subscription',
        ),
    ]

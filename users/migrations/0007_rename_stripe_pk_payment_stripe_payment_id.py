# Generated by Django 4.2.3 on 2023-08-16 09:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_rename_stripe_id_payment_stripe_pk'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='stripe_pk',
            new_name='stripe_payment_id',
        ),
    ]

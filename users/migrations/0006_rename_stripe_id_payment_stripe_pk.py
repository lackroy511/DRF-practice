# Generated by Django 4.2.3 on 2023-08-16 09:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_payment_stripe_pk_payment_stripe_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='stripe_id',
            new_name='stripe_pk',
        ),
    ]

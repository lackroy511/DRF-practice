# Generated by Django 4.2.3 on 2023-08-20 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_payment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateField(blank=True, null=True, verbose_name='дата последнего входа'),
        ),
    ]

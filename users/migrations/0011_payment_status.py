# Generated by Django 4.2.3 on 2023-08-16 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_payment_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.CharField(default='open', max_length=10, verbose_name='статус платежа'),
        ),
    ]

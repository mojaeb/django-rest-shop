# Generated by Django 3.2.8 on 2021-10-20 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_order_payment_succeed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='cart',
            new_name='order',
        ),
    ]

# Generated by Django 3.2.8 on 2021-10-29 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0036_remove_order_payment_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='show_in_home',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
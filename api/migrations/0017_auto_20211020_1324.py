# Generated by Django 3.2.8 on 2021-10-20 09:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_remove_address_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='is_mine',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='address',
            name='person_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='phone_number',
            field=models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]

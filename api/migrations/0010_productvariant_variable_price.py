# Generated by Django 3.2.8 on 2021-12-13 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_remove_productvariant_variable_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='productvariant',
            name='variable_price',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 3.2.8 on 2021-11-14 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_registerdraft'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registerdraft',
            name='user_data',
            field=models.JSONField(blank=None, null=True),
        ),
    ]

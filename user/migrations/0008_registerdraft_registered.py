# Generated by Django 3.2.8 on 2021-11-15 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_registerdraft_user_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='registerdraft',
            name='registered',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 3.2.8 on 2021-11-15 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_rename_user_data_registerdraft_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registerdraft',
            old_name='data',
            new_name='form',
        ),
    ]
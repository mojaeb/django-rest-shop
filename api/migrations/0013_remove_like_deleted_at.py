# Generated by Django 3.2.8 on 2021-10-18 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_like_deleted_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='deleted_at',
        ),
    ]
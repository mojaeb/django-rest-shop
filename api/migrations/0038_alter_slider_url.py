# Generated by Django 3.2.8 on 2021-10-29 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0037_category_show_in_home'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slider',
            name='url',
            field=models.CharField(max_length=200),
        ),
    ]
# Generated by Django 3.2.8 on 2021-10-16 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_product_image_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='image_url',
            new_name='image',
        ),
    ]

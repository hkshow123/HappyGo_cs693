# Generated by Django 5.0 on 2023-12-18 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_remove_category_level_remove_category_lft_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producttype',
            old_name='product_category_id',
            new_name='category_id',
        ),
    ]
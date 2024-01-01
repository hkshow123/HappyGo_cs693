# Generated by Django 5.0 on 2023-12-22 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_remove_product_update_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productinventory',
            name='store_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, error_messages={'name': {'max_length': 'the price must be greater than or equal to 999.99'}}, help_text='format:maximum price 999.99', max_digits=5, null=True, verbose_name='recommended price'),
        ),
    ]

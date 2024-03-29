# Generated by Django 5.0 on 2023-12-22 20:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_alter_productinventory_store_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productinventory',
            name='product_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='product_id', to='inventory.product', unique=True, verbose_name='product id'),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('location', models.CharField(max_length=20, verbose_name='location')),
                ('upc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='upc_location', to='inventory.productinventory', to_field='upc', unique=True, verbose_name='product upc')),
            ],
        ),
        migrations.AlterField(
            model_name='productinventory',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.location'),
        ),
        migrations.DeleteModel(
            name='Stock',
        ),
    ]

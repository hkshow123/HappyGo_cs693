# Generated by Django 5.0 on 2023-12-26 17:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=30, unique=True, verbose_name='User name')),
                ('password', models.CharField(max_length=20, verbose_name='password')),
                ('email', models.EmailField(max_length=20, unique=True, verbose_name='email address')),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='format:required,unique,max-255', max_length=30, unique=True, verbose_name='brand name')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='format:Y-m-d H:M:S', verbose_name='created at')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='format:required,max-100', max_length=100, verbose_name='category name')),
            ],
            options={
                'verbose_name': 'product category',
                'verbose_name_plural': 'product categories',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=20, verbose_name='location')),
                ('is_active', models.BooleanField(default=True, help_text='format:true=product visible', verbose_name='Location availability')),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=100, verbose_name='url')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=30, unique=True, verbose_name='User name')),
                ('password', models.CharField(max_length=20, verbose_name='password')),
                ('email', models.EmailField(max_length=20, unique=True, verbose_name='email address')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upc', models.CharField(help_text='format:required,unique', max_length=50, null=True, unique=True, verbose_name='product upc')),
                ('name', models.CharField(help_text='format:required,max-100', max_length=100, verbose_name='product name')),
                ('description', models.TextField(help_text='format:required,max-100', max_length=255, verbose_name='product description')),
                ('is_active', models.BooleanField(default=True, help_text='format:true=product visible', verbose_name='Product visibility')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='format:Y-m-d H:M:S', verbose_name='created at')),
                ('weight', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='weight of product')),
                ('brand_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.brand', verbose_name='brand')),
                ('media_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.media', verbose_name='pictures')),
            ],
        ),
        migrations.CreateModel(
            name='ProductInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upc', models.CharField(default=1, help_text='format:required,unique,max-12', max_length=12, unique=True, verbose_name='universal product code')),
                ('is_active', models.BooleanField(default=True, help_text='format:true=product visible', verbose_name='product visibility_in')),
                ('retail_price', models.DecimalField(blank=True, decimal_places=2, default=0, error_messages={'name': {'max_length': 'the price must be greater than or equal to 999.99'}}, help_text='format:maximum price 999.99', max_digits=5, null=True, verbose_name='recommended price')),
                ('store_price', models.DecimalField(blank=True, decimal_places=2, default=0, error_messages={'name': {'max_length': 'the price must be greater than or equal to 999.99'}}, help_text='format:maximum price 999.99', max_digits=5, null=True, verbose_name='recommended price')),
                ('weight', models.FloatField(default=0, verbose_name='product weight')),
                ('update_at', models.DateTimeField(auto_now=True, help_text='format:Y-m-d H:M:S', verbose_name='last update at')),
                ('total', models.IntegerField(default=0, verbose_name='Total')),
                ('brand_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='brand', to='inventory.brand', verbose_name='brand id')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.location')),
                ('product_id', models.OneToOneField(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='product_id', to='inventory.product', verbose_name='product id')),
                ('product_name', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='product_name', to='inventory.product', verbose_name='product name')),
            ],
        ),
        migrations.AddField(
            model_name='media',
            name='upc',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.productinventory'),
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='format:product,unique,max-255', max_length=255, unique=True, verbose_name='type of product')),
                ('category_id', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='inventory.category')),
            ],
        ),
        migrations.AddField(
            model_name='productinventory',
            name='product_type_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='product_type', to='inventory.producttype', verbose_name='product type'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_type_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.producttype', verbose_name='product type'),
        ),
    ]

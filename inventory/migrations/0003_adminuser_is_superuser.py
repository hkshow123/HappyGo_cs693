# Generated by Django 5.0 on 2023-12-26 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_adminuser_is_admin_adminuser_last_login_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminuser',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]

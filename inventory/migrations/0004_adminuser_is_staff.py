# Generated by Django 5.0 on 2023-12-26 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_adminuser_is_superuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]

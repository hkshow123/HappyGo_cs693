# Generated by Django 5.0 on 2023-12-28 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_remove_profiles_email_remove_profiles_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profiles',
            name='city',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AddField(
            model_name='profiles',
            name='state',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AddField(
            model_name='profiles',
            name='street_address',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AddField(
            model_name='profiles',
            name='telephone',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AddField(
            model_name='profiles',
            name='zipcode',
            field=models.CharField(blank=True, max_length=5),
        ),
    ]

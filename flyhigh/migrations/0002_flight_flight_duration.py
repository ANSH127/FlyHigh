# Generated by Django 4.1.5 on 2023-01-24 14:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('flyhigh', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flight',
            name='flight_duration',
            field=models.TimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]

# Generated by Django 4.1.5 on 2023-01-27 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flyhigh', '0006_alter_booking_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='f_name',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='l_name',
        ),
        migrations.AddField(
            model_name='booking',
            name='contact_details',
            field=models.CharField(default='', max_length=500),
        ),
    ]
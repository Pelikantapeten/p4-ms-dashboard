# Generated by Django 3.2.13 on 2022-08-09 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_auto_20220809_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentsession',
            name='time_spent',
            field=models.IntegerField(choices=[(15, '15 minutes'), (30, '30 minutes'), (45, '45 minutes'), (60, '60 minutes')], default=15, help_text='Lenght of session', verbose_name='Length of session'),
        ),
    ]
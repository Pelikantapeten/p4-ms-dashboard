# Generated by Django 3.2.13 on 2022-08-19 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_studentsession_time_spent'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentsession',
            name='project_link',
            field=models.URLField(blank=True, verbose_name='Projent URL'),
        ),
        migrations.AddField(
            model_name='studentsession',
            name='project_repo',
            field=models.URLField(blank=True, verbose_name='Project repository'),
        ),
    ]
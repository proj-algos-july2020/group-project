# Generated by Django 2.2 on 2020-08-01 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kosbiz_app', '0012_auto_20200721_2304'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='address',
        ),
        migrations.RemoveField(
            model_name='user',
            name='birthday',
        ),
        migrations.RemoveField(
            model_name='user',
            name='gender',
        ),
    ]

# Generated by Django 2.2 on 2020-07-19 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kosbiz_app', '0008_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='businesses',
            field=models.ManyToManyField(related_name='categories', to='kosbiz_app.Business'),
        ),
    ]
# Generated by Django 2.2 on 2020-07-19 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kosbiz_app', '0007_business_image_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('businesses', models.ManyToManyField(to='kosbiz_app.Business')),
            ],
        ),
    ]

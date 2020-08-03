# Generated by Django 2.2 on 2020-07-20 21:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kosbiz_app', '0010_auto_20200720_2351'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessreviews',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='review_user', to='kosbiz_app.User'),
            preserve_default=False,
        ),
    ]

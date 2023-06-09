# Generated by Django 4.2.1 on 2023-06-01 17:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import time


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='StravaToken',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='strava', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('token_type', models.CharField(max_length=250)),
                ('uid', models.CharField(max_length=250)),
                ('auth_time', models.FloatField(default=time.time)),
                ('expires_in', models.FloatField()),
                ('expires_at', models.FloatField()),
                ('access_token', models.CharField(max_length=250)),
                ('refresh_token', models.CharField(max_length=250)),
            ],
        ),
    ]

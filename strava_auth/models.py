import time

from django.contrib.auth.models import User
from django.db import models


class StravaToken(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='strava'
    )
    token_type = models.CharField(max_length=250)
    uid = models.CharField(max_length=250)
    auth_time = models.FloatField(default=time.time)
    expires_in = models.FloatField()
    expires_at = models.FloatField()
    access_token = models.CharField(max_length=250)
    refresh_token = models.CharField(max_length=250)
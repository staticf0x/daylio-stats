from django.contrib.auth.models import User
from django.db import models


class UserSettings(models.Model):
    """Settings for an individual user."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    save_notes = models.BooleanField(default=True)


class Entry(models.Model):
    """Journal entry"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    mood = models.CharField(max_length=64)
    activities = models.CharField(max_length=256)
    notes = models.TextField()

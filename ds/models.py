"""App models."""

from django.contrib.auth.models import User
from django.db import models


class UserSettings(models.Model):
    """Settings for an individual user."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    save_notes = models.BooleanField(default=True)

    def __str__(self):
        return f'UserSettings ({self.id}, {self.user})'


class Activity(models.Model):
    """
    Activity for an Entry for a User.
    The reason there's a User reference is for the situation
    when a user wants to delete all their data (incl. activities).
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'Activity ({self.id}, {self.user}): {self.name}'


class Entry(models.Model):
    """Journal entry."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    mood_name = models.CharField(max_length=64)
    mood = models.IntegerField()
    activities = models.ManyToManyField(Activity)
    notes = models.TextField()

    def __str__(self):
        return f'Entry ({self.id}, {self.user}): {self.datetime} {self.mood_name}'

"""App models."""

from daylio_parser.config import DEFAULT_MOODS
from daylio_parser.parser import Entry as DpEntry
from django.contrib.auth.models import User
from django.db import models


def get_default_moods():
    """Callable for default on mood_config field."""

    return DEFAULT_MOODS.copy()


class UserSettings(models.Model):
    """Settings for an individual user."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    save_notes = models.BooleanField(default=True)
    mood_config = models.JSONField(default=get_default_moods)

    def __str__(self):
        return f'UserSettings ({self.id}, {self.user})'


class EntryActivities(models.Model):
    """
    Custom join model for Activity and Entry.
    This is needed for quick operations on user's data (bulk delete).
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE)
    entry = models.ForeignKey('Entry', on_delete=models.CASCADE)

    class Meta:
        db_table = 'ds_entry_activities'


class Activity(models.Model):
    """
    Activity for an Entry for a User.
    The reason there's a User reference is for the situation
    when a user wants to delete all their data (incl. activities).
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)

    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        return f'Activity ({self.id}, {self.user}): {self.name}'


class Entry(models.Model):
    """Journal entry."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    mood_name = models.CharField(max_length=64)
    mood = models.IntegerField()
    activities = models.ManyToManyField(Activity, through=EntryActivities)
    notes = models.TextField()

    def __str__(self):
        return f'Entry ({self.id}, {self.user}): {self.datetime} {self.mood_name}'

"""Utilities for converting entries between daylio_parser and models."""

from daylio_parser.config import MoodConfig
from daylio_parser.parser import Entry

from ds import models

from .data import get_user_settings


class EntryConverter:
    def __init__(self, user):
        self.user = user
        self.settings = get_user_settings(user)
        self.mood_config = MoodConfig(self.settings.mood_config)

    def get_entries(self):
        """Convert stored DB entries into Entry objects for daylio_parser."""

        db_entries = (
            models.Entry.objects.filter(user=self.user)
            .order_by('datetime')
            .prefetch_related('activities')
        )

        entries = []

        for db_entry in db_entries:
            # TODO: We need tzinfo saved either in user settings
            # or for each entry
            entry = Entry(
                db_entry.datetime,
                self.mood_config.get(db_entry.mood_name),
                [a.name for a in db_entry.activities.all()],
                db_entry.notes,
            )

            entries.append(entry)

        return entries

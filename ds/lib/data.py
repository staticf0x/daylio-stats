"""Basic data operations."""

import codecs
import io
from typing import List

from daylio_parser.parser import Entry, Parser
from django.db import connection, transaction

from ds import models


def get_entries_from_upload(file_field) -> List[Entry]:
    """Return entries from an uploaded CSV file."""

    # Write the uploaded file into a buffer
    buf = io.BytesIO()

    for chunk in file_field.chunks():
        buf.write(chunk)

    buf.seek(0)

    # Convert to StringIO so the CSV reader can iterate over strings and not bytes
    stream_reader = codecs.getreader('utf-8')
    wrapped_file = stream_reader(buf)

    # Load the CSV
    parser = Parser()
    entries = parser.load_from_buffer(wrapped_file)
    buf.close()

    return entries


def get_user_settings(user) -> models.UserSettings:
    """Return UserSettings for a given user."""

    return models.UserSettings.objects.get(user=user)


class UserDataImport:
    """A class to import user data (entries from CSV)."""

    def __init__(self, user):
        self.user = user
        self.settings = get_user_settings(user)

    def import_entries(self, entries: List[Entry]) -> None:
        """Import entries for a user."""

        self.__delete_existing()
        self.__import_activities(entries)
        db_entries = self.__import_entries(entries)
        self.__set_activities(entries, db_entries)

    def __delete_existing(self):
        """Delete all existing data for the user."""

        # The reason this is done in raw SQL is that we need the to
        # delete the data quickly, without ORM checking the cascade
        # to delete (it's emulated in Django and takes some time
        # and produces a lot of queries).
        # See models.EntryActivities

        with connection.cursor() as cur:
            cur.execute('DELETE FROM ds_entry_activities WHERE user_id = %s', [self.user.id])
            cur.execute('DELETE FROM ds_activity WHERE user_id = %s', [self.user.id])
            cur.execute('DELETE FROM ds_entry WHERE user_id = %s', [self.user.id])

    def __import_activities(self, entries: List[Entry]):
        """Import activities from entries (unique)."""

        # Make activities unique
        activities = set()

        for entry in entries:
            activities |= set(entry.activities)

        # Import
        with transaction.atomic():
            to_import = []

            for activity in activities:
                db_activity = models.Activity()
                db_activity.user = self.user
                db_activity.name = activity

                to_import.append(db_activity)

            models.Activity.objects.bulk_create(to_import)

    def __import_entries(self, entries: List[Entry]):
        """Import all entries."""

        save_notes = self.settings.save_notes

        with transaction.atomic():
            to_import = []

            for entry in entries:
                db_entry = models.Entry()
                db_entry.user = self.user
                db_entry.datetime = entry.datetime
                db_entry.mood_name = entry.mood.name
                db_entry.mood = entry.mood.level

                if save_notes:
                    db_entry.notes = entry.notes

                to_import.append(db_entry)

            models.Entry.objects.bulk_create(to_import)

        # Return all new entries sorted by datetime (same order as input entries)
        return models.Entry.objects.filter(user=self.user).order_by('datetime')

    def __set_activities(self, entries: List[Entry], db_entries):
        """
        Import a many-to-many relationship between entries (db_entries)
        and activities (through entries and Activity objects).
        """

        # Activity LUT
        activities = {obj.name: obj for obj in models.Activity.objects.filter(user=self.user)}

        to_import = []

        for entry, db_entry in zip(entries, db_entries):
            id_entry = db_entry.id

            for activity in entry.activities:
                db_activity = activities[activity]

                id_activity = db_activity.id
                id_user = self.user.id

                # Create the connecting entry (EntryActivities)
                through_obj = models.Entry.activities.through(
                    entry_id=id_entry,
                    activity_id=id_activity,
                    user_id=id_user
                )

                to_import.append(through_obj)

        models.Entry.activities.through.objects.bulk_create(to_import)

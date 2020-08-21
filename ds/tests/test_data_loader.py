# -*- coding: utf-8 -*-
"""
Test the DataLoader class
"""

import datetime
import os

from django.test import TestCase

from dayliostats.settings import BASE_DIR
from ds.lib.data import DataLoader


class TestDataLoader(TestCase):
    """
    Tests for the DataLoader class
    """

    def setUp(self):
        """
        Create the DataLoader
        """

        self.dl = DataLoader(os.path.join(BASE_DIR, 'ds', 'tests', 'data', 'test_data.csv'))
        self.dl.load()

    def test_load_all_data(self):
        """
        Test that all data is loaded
        """

        data = self.dl.avg_moods

        self.assertEqual(len(data), 5)

    def test_average_moods(self):
        """
        Test average moods in the first and last day
        """

        data = self.dl.avg_moods

        first_day = data[0]
        last_day = data[-1]

        self.assertEqual(first_day[0], datetime.datetime(2020, 5, 25))
        self.assertEqual(first_day[1], 2)

        self.assertEqual(last_day[0], datetime.datetime(2020, 5, 30))
        self.assertEqual(last_day[1], 5)

    def test_entries(self):
        """
        Test loading all entries
        """

        entries = self.dl.entries

        first_entry = entries[0]

        self.assertEqual(first_entry.datetime, datetime.datetime(2020, 5, 25, 7, 9))
        self.assertEqual(first_entry.mood, 3)
        self.assertEqual(first_entry.mood_str, 'meh')
        self.assertEqual(first_entry.activities, [])
        self.assertEqual(first_entry.notes, '')

        full_entry = entries[8]

        self.assertEqual(full_entry.datetime, datetime.datetime(2020, 5, 27, 12, 20))
        self.assertEqual(full_entry.mood, 4)
        self.assertEqual(full_entry.mood_str, 'good')
        self.assertEqual(full_entry.activities, ['work', 'good meal'])
        self.assertEqual(full_entry.notes, 'Just good')

    def test_both_hour_formats(self):
        """
        Test that both 12 and 24 hour formats are parsed
        """

        entries = self.dl.entries

        entry_12h = entries[0]
        entry_24h = entries[1]

        self.assertEqual(entry_12h.datetime, datetime.datetime(2020, 5, 25, 7, 9))
        self.assertEqual(entry_24h.datetime, datetime.datetime(2020, 5, 25, 14, 58))

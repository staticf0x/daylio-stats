# -*- coding: utf-8 -*-
"""
Test the DataLoader class
"""

import os
import datetime
from django.test import TestCase
from ds.lib.data import DataLoader
from dayliostats.settings import BASE_DIR


class TestsDataLoader(TestCase):
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

        self.assertEquals(len(data), 3)

    def test_average_moods(self):
        """
        Test average moods in the first and last day
        """

        data = self.dl.avg_moods

        first_day = data[0]
        last_day = data[-1]

        self.assertEquals(first_day[0], datetime.datetime(2020, 5, 25))
        self.assertEquals(first_day[1], 2)

        self.assertEquals(last_day[0], datetime.datetime(2020, 5, 28))
        self.assertEquals(last_day[1], 4.6)

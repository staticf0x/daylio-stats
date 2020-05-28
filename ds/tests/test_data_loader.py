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
    def test_load_csv(self):
        dl = DataLoader(os.path.join(BASE_DIR, 'ds', 'tests', 'data', 'test_data.csv'))
        data = dl.load()

        first_day = data[0]
        last_day = data[-1]

        self.assertEquals(first_day[0], datetime.datetime(2020, 5, 25))
        self.assertEquals(first_day[1], 2)

        self.assertEquals(last_day[0], datetime.datetime(2020, 5, 28))
        self.assertEquals(last_day[1], 4.6)

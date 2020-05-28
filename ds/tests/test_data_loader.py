# -*- coding: utf-8 -*-
"""
Test the DataLoader class
"""

import os
from django.test import TestCase
from ds.lib.data import DataLoader
from dayliostats.settings import BASE_DIR


class TestsDataLoader(TestCase):
    def test_load_csv(self):
        dl = DataLoader(os.path.join(BASE_DIR, 'ds', 'tests', 'data', 'test_data.csv'))
        data = dl.load()

        self.assertEquals(data[0][1], 2)  # First entry avg mood
        self.assertEquals(data[-1][1], 4.6)  # Last entry avg mood

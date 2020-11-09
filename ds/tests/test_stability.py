# -*- coding: utf-8 -*-
"""
Test the Stability class
"""

import os

from django.test import TestCase

from dayliostats.settings import BASE_DIR
from ds.lib.data import DataLoader
from ds.lib.stability import Stability


class TestStability(TestCase):
    def setUp(self):
        """
        Create the DataLoader
        """

        self.dl = DataLoader(os.path.join(BASE_DIR, 'ds', 'tests', 'data', 'test_data.csv'))
        self.dl.load()

    def test_stability_by_month(self):
        stability = Stability(self.dl)

        self.assertEqual(stability.stability_by_month(2020, 5), 0.75)

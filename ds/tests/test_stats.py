# -*- coding: utf-8 -*-
"""
Test the Stats class
"""

import os
import datetime
import numpy as np
from django.test import TestCase
from ds.lib.data import DataLoader
from ds.lib.stats import Stats
from dayliostats.settings import BASE_DIR


class TestStats(TestCase):
    def setUp(self):
        """
        Create the DataLoader
        """

        self.dl = DataLoader(os.path.join(BASE_DIR, 'ds', 'tests', 'data', 'test_data.csv'))
        self.dl.load()
        self.stats = Stats(self.dl.avg_moods)

    def test_data_loaded(self):
        """
        Test that all data loaded into Stats class
        """

        data = self.stats._Stats__avg_moods

        expected_data = [
            (datetime.datetime(2020, 5, 25), 2),
            # Missing day in CSV
            (datetime.datetime(2020, 5, 27), 4.3),
            (datetime.datetime(2020, 5, 28), 4.6),
            (datetime.datetime(2020, 5, 29), 5.0),
            (datetime.datetime(2020, 5, 30), 5.0),
        ]

        self.assertEquals(len(data), 5)
        self.assertEquals(data, expected_data)

    def test_rolling_mean_2(self):
        """
        Test rolling mean of data for N=2
        """

        data = self.stats.rolling_mean(2)

        expected_data = [
            (datetime.datetime(2020, 5, 25), np.nan),
            # Missing day in CSV
            (datetime.datetime(2020, 5, 27), 3.15),
            (datetime.datetime(2020, 5, 28), 4.45),
            (datetime.datetime(2020, 5, 29), 4.8),
            (datetime.datetime(2020, 5, 30), 5.0),
        ]

        self.__assert_rolling_mean_data_equal(data, expected_data)

    def test_rolling_mean_5(self):
        """
        Test rolling mean of data for N=5
        """

        data = self.stats.rolling_mean(5)

        expected_data = [
            (datetime.datetime(2020, 5, 25), np.nan),
            # Missing day in CSV
            (datetime.datetime(2020, 5, 27), np.nan),
            (datetime.datetime(2020, 5, 28), np.nan),
            (datetime.datetime(2020, 5, 29), np.nan),
            (datetime.datetime(2020, 5, 30), 4.18),
        ]

        self.__assert_rolling_mean_data_equal(data, expected_data)

    def __assert_rolling_mean_data_equal(self, data, expected_data):
        """
        Compare two arrays of (datetime, avg_mood)
        """

        for first, second in zip(data, expected_data):
            self.assertEquals(first[0], second[0])

            if np.isnan(first[1]):
                self.assertTrue(np.isnan(first[1]))
                self.assertTrue(np.isnan(second[1]))
            else:
                self.assertAlmostEquals(first[1], second[1], 2)
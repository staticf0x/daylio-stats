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
    """
    Tests for the Stats class
    """

    def setUp(self):
        """
        Create the DataLoader
        """

        self.dl = DataLoader(os.path.join(BASE_DIR, 'ds', 'tests', 'data', 'test_data.csv'))
        self.dl.load()
        self.stats = Stats(self.dl.avg_moods)
        self.stats.interpolate_steps = 4

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

        self.assertEqual(len(data), 5)
        self.assertEqual(data, expected_data)

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

        self.__assert_mood_data_equal(data, expected_data)

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

        self.__assert_mood_data_equal(data, expected_data)

    def test_interpolate(self):
        # Use raw data
        data = self.stats._Stats__avg_moods
        dates, moods = self.stats.interpolate(data)

        actual_data = zip(dates, moods)
        expected_data = [
            (datetime.datetime(2020, 5, 25, 0, 0), 2),
            (datetime.datetime(2020, 5, 25, 6, 0), 2.575),
            (datetime.datetime(2020, 5, 25, 12, 0), 3.15),
            (datetime.datetime(2020, 5, 25, 18, 0), 3.725),
            (datetime.datetime(2020, 5, 27, 0, 0), 4.3),
            (datetime.datetime(2020, 5, 27, 6, 0), 4.375),
            (datetime.datetime(2020, 5, 27, 12, 0), 4.45),
            (datetime.datetime(2020, 5, 27, 18, 0), 4.525),
            (datetime.datetime(2020, 5, 28, 0, 0), 4.6),
            (datetime.datetime(2020, 5, 28, 6, 0), 4.7),
            (datetime.datetime(2020, 5, 28, 12, 0), 4.8),
            (datetime.datetime(2020, 5, 28, 18, 0), 4.9),
            (datetime.datetime(2020, 5, 29, 0, 0), 5.0),
            (datetime.datetime(2020, 5, 29, 6, 0), 5.0),
            (datetime.datetime(2020, 5, 29, 12, 0), 5.0),
            (datetime.datetime(2020, 5, 29, 18, 0), 5.0),
            (datetime.datetime(2020, 5, 30, 0, 0), 5.0),
            (datetime.datetime(2020, 5, 30, 6, 0), 5.0),
            (datetime.datetime(2020, 5, 30, 12, 0), 5.0),
            (datetime.datetime(2020, 5, 30, 18, 0), 5.0),
            (datetime.datetime(2020, 5, 31, 0, 0), 5.0),
        ]

        self.__assert_mood_data_equal(actual_data, expected_data)

    def test_avg(self):
        """
        Test mean and std values
        """

        mean, std = self.stats.mean()

        self.assertAlmostEquals(mean, 4.18, 2)
        self.assertAlmostEquals(std, 1.12, 2)

    def __assert_mood_data_equal(self, data, expected_data):
        """
        Compare two arrays of (datetime, avg_mood)
        """

        self.assertEqual(len(list(data)), len(list(expected_data)))

        for first, second in zip(data, expected_data):
            self.assertEqual(first[0], second[0])

            if np.isnan(first[1]):
                self.assertTrue(np.isnan(first[1]))
                self.assertTrue(np.isnan(second[1]))
            else:
                self.assertAlmostEquals(first[1], second[1], 3)

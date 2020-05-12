# -*- coding: utf-8 -*-
"""
Data loader
"""

import csv
import datetime
import numpy as np
from ds import config


class DataLoader:
    """
    A class for loading the raw data and converting to something more usable
    """

    def __init__(self, path):
        self.__csv_path = path
        self.__raw_data = {}
        self.__avg_moods = []

    def load(self):
        """
        Load the raw data and compute average moods
        """

        self.__load_raw_data()
        self.__compute_avg_moods()

        return self.__avg_moods

    def __load_raw_data(self):
        """
        Read mood data from CSV file
        """

        data_tmp = {}

        with open(self.__csv_path) as fread:
            csv_reader = csv.reader(fread, delimiter=',', quotechar='"')
            next(csv_reader)  # Skip header

            for row in csv_reader:
                date = row[0]
                mood_str = row[4]
                mood = config.MOODS[mood_str]

                data_tmp.setdefault(date, [])
                data_tmp[date].append(mood)

        self.__raw_data = data_tmp

    def __compute_avg_moods(self):
        """
        Go through the raw data (date: mood list) and compute average
        values for each day
        """

        data = []

        for date, moods_raw in self.__raw_data.items():
            dt = datetime.datetime.strptime(date, '%Y-%m-%d')
            mood_avg = np.mean(moods_raw)

            data.append((dt, mood_avg))

        data.reverse()

        self.__avg_moods = data

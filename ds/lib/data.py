# -*- coding: utf-8 -*-
"""
Data loader
"""

import csv
import datetime
import numpy as np
from ds.lib import config


class DataLoader:
    """
    A class for loading the raw data and converting to something more usable
    """

    def __init__(self, path):
        self.__csv_path = '';
        self.__buf = None

        if isinstance(path, str):
            self.__csv_path = path
        else:
            # Let's accept also BytesIO
            self.__buf = path

        self.__raw_data = {}
        self.avg_moods = []

    def load(self):
        """
        Load the raw data and compute average moods
        """

        self.__load_raw_data()
        self.__compute_avg_moods()

        return self.avg_moods

    def __load_raw_data(self):
        """
        Read mood data from CSV file

        WARNING: Daylio saves the time in either 12 or 24 hour format
        so if we later need also time, be warned
        """

        print('Loading source data...')

        data_tmp = {}

        fread = self.__buf if self.__buf else open(self.__csv_path, 'r')

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

        print('Computing average moods...')

        data = []

        for date, moods_raw in self.__raw_data.items():
            dt = datetime.datetime.strptime(date, '%Y-%m-%d')
            mood_avg = np.mean(moods_raw)

            data.append((dt, mood_avg))

        data.reverse()

        self.avg_moods = data

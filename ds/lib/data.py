# -*- coding: utf-8 -*-
"""
Data loader
"""

import csv
import datetime
from dataclasses import dataclass
from typing import List
import numpy as np
from ds.lib import config


@dataclass
class Entry:
    """
    Data for one day
    """

    datetime: datetime.datetime
    mood: float
    mood_str: str
    activities: List[str]
    notes: str


class DataLoader:
    """
    A class for loading the raw data and converting to something more usable
    """

    def __init__(self, path):
        self.__csv_path = ''
        self.__buf = None

        if isinstance(path, str):
            self.__csv_path = path
        else:
            # Let's accept also BytesIO
            self.__buf = path

        self.__raw_data = {}
        self.avg_moods = []
        self.entries = []

    def load(self):
        """
        Load the raw data and compute average moods
        """

        self.__load_raw_data()
        self.__compute_avg_moods()

    def __load_raw_data(self):
        """
        Read mood data from CSV file
        """

        data_tmp = {}

        fread = self.__buf if self.__buf else open(self.__csv_path, 'r')

        csv_reader = csv.reader(fread, delimiter=',', quotechar='"')
        next(csv_reader)  # Skip header

        for row in csv_reader:
            # Raw data
            date_str = row[0]
            time_str = row[3]
            mood_str = row[4]
            activities = row[5]
            notes = row[6]

            # Get mood as int
            mood = config.MOODS[mood_str]

            # Add to raw data dict
            data_tmp.setdefault(date_str, [])
            data_tmp[date_str].append(mood)

            # Create entry object
            dt = datetime.datetime.strptime(date_str, '%Y-%m-%d')

            try:
                t = datetime.datetime.strptime(time_str, '%I:%M %p')
            except ValueError:
                t = datetime.datetime.strptime(time_str, '%H:%M')

            # TODO: There has to be a better way
            t = datetime.time(hour=t.hour, minute=t.minute)
            dt = dt.combine(dt, t)

            entry = Entry(
                dt,
                mood,
                mood_str,
                [] if activities == '' else activities.split(' | '),
                notes
            )
            self.entries.append(entry)

        self.__raw_data = data_tmp
        self.entries.reverse()

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

        self.avg_moods = data

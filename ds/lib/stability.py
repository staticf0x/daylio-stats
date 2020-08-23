# -*- coding: utf-8 -*-
"""
Stats class for calculating mood stability
"""

import datetime
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np


class Stability:
    """
    Counts mood stability and provides a chart of stability

    TODO: Add tests
    """

    def __init__(self, loader):
        self.__loader = loader

    def __stability_percent(self, x):
        """
        Compute mood stability for an input of mood count.

        For example:
            Mood count in a day: [ 1,  2,  3, 4, 5]
            Input:               [50, 20, 10, 2, 1]
            Output:              84.94%
        """

        return (1*x[0] + .75*x[1] + .5*x[2] + .25*x[3] + 0*x[4])/sum(x)

    def stability_by_month(self, year, month):
        """
        Returns a stability percentage [0, 1] for a given year/month
        """

        group_by_date = self.__loader.get_raw_data(year, month)

        # Count number of moods per date
        count_by_date = {}

        for date_str, moods in group_by_date.items():
            count_by_date[date_str] = len(Counter(moods))

        # Total days in the export
        total_days = len(count_by_date)

        # Count the days where N number of moods occur
        mood_counts = Counter(count_by_date.values())
        mood_counts_list = [0, 0, 0, 0, 0]

        print(f'{year}-{month}')
        print('Mood count   Days   Days/Total days')

        # TODO: We might use this information later,
        # how many percent of days had 1 mood, 2 moods, etc
        for mood_count, count in sorted(mood_counts.items()):
            perc = count/total_days
            mood_counts_list[mood_count - 1] = count

            print(f'{mood_count}            {count:4d}   {perc:6.2%}')

        print()

        # Calculate mood stability
        mood_stability = self.__stability_percent(mood_counts_list)

        return mood_stability

    def stability(self):
        """
        Returns dates and corresponding stabilities for the whole
        range of data
        """

        raw_data = self.__loader.get_raw_data()

        filters = []

        # Find all year/month pairs
        for key in raw_data.keys():
            key_split = [int(x) for x in key.split('-')]
            date_filter = (key_split[0], key_split[1])

            if date_filter not in filters:
                filters.append(date_filter)

        dates = []
        stabilities = []

        # Calculate stability for each year/month
        for year, month in reversed(filters):
            stability_perc = self.stability_by_month(year, month)*100

            dt = datetime.datetime(year, month, 1)

            dates.append(dt)
            stabilities.append(stability_perc)

        return dates, stabilities

    def stability_plot(self):
        """
        Creates a chart of stability percentages over time
        """

        dates, stabilities = self.stability()

        _, axes = plt.subplots(1, 1, figsize=(12, 4))

        axes.plot(dates, stabilities)
        axes.set_title('Mood stability over time')
        axes.set_xlabel('Date')
        axes.set_ylabel('Mood stability (%)')
        axes.grid()

        plt.tight_layout()
        plt.show()

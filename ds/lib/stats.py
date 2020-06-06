# -*- coding: utf-8 -*-
"""
A class to compute stats, interpolate data and so on.
"""

import datetime
import numpy as np
from ds.lib import config


class Stats:
    """
    A class to compute stats, interpolate data and so on.
    """

    def __init__(self, avg_moods):
        self.__avg_moods = avg_moods
        self.interpolate_steps = 12

    def split_into_bands(self, moods):
        split_data = dict.fromkeys(config.BOUNDARIES.keys())

        for mood_name, boundaries in config.BOUNDARIES.items():
            # boundaries is a tuple of (low, high)
            # Upper bound
            masked_data = np.ma.masked_where(moods >= boundaries[1], moods)

            # Lower bound -- already working with partly masked data
            masked_data = np.ma.masked_where(moods < boundaries[0], masked_data)

            split_data[mood_name] = masked_data

        return split_data

    def interpolate(self, avg_moods):
        """
        Interpolate missing values between midnights
        """

        steps = int(self.interpolate_steps)

        if steps > 1440:
            raise ValueError('Max number of steps is 1440')

        dates = []
        moods = []
        step = 1440//steps  # Step size in minutes

        for i in range(len(avg_moods)):  # pylint: disable=consider-using-enumerate
            current_point = avg_moods[i]

            if np.isnan(current_point[1]):
                continue

            try:
                next_point = avg_moods[i + 1]
            except IndexError:
                # Add last day as the date on midnight
                next_time = datetime.time(hour=0, minute=0)
                next_dt = current_point[0].combine(current_point[0], next_time)

                dates.append(next_dt)
                moods.append(current_point[1])

                # break

            value_diff = next_point[1] - current_point[1]  # Mood difference between days
            time_diff = steps  # Time difference a.k.a. number of buckets
            coef = value_diff/time_diff  # How much the mood changes in one step

            for step_n in range(0, steps):
                # Simple linear interpolation
                next_value = step_n*coef + current_point[1]

                # step*step_n == number of minutes in the current day
                # just split it into hours and minutes for time object
                hour = 0 if step_n == 0 else (step*step_n)//60
                minute = 0 if step_n == 0 else (step*step_n)%60

                next_time = datetime.time(hour=int(hour), minute=int(minute))
                next_dt = current_point[0].combine(current_point[0], next_time)

                dates.append(next_dt)
                moods.append(next_value)

        return np.array(dates), np.array(moods)

    def rolling_mean(self, N=5):
        data = np.array(self.__avg_moods)

        # Compute the rolling mean for our data
        # Moods are stored in the 1st column, dates in 0th
        filtered_data = np.convolve(data[:, 1], np.ones((N, ))/N, mode='valid')
        filtered_data = filtered_data.astype(np.float64).round(2)

        # Fill the missing entries with NaN,
        # so we can replace the original column
        # with filtered data
        nans = np.zeros(N - 1)
        nans[:] = np.nan
        filtered_data = np.concatenate((nans, filtered_data))
        data[:, 1] = filtered_data

        return data

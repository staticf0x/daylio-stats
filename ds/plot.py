# -*- coding: utf-8 -*-
"""
A class for plotting the data
"""

import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
from ds import config


class Plot:
    """
    A class for interpolating and plotting the data
    """

    def __init__(self, avg_moods):
        self.__avg_moods = avg_moods
        self.interpolate_steps = 720  # Number of steps per day
        self.__dates = None
        self.__moods = None
        self.__masked_data = dict.fromkeys(config.BOUNDARIES.keys())

    def plot_average_moods(self, output_name=None):
        """
        Plot the average mood data into a PNG file
        """

        if not output_name:
            output_name = 'daylio-plot-{}.png'.format(time.strftime('%Y-%m-%d-%H%M%S'))

        self.__interpolate()
        self.__split_into_bands()

        fig, ax = plt.subplots(1, 1, figsize=(12, 4))

        plot_args = []

        for mood_name, color in config.COLORS.items():
            plot_args.append(self.__dates)
            plot_args.append(self.__masked_data[mood_name])
            plot_args.append(color)

        ax.plot(*plot_args)

        ax.set_xlabel('Date')
        ax.set_ylabel('Mood')
        ax.set_yticks(np.arange(1, len(config.MOODS) + 1, 1))
        plt.grid()

        plt.savefig(output_name, dpi=120)

    def __interpolate(self):
        """
        Interpolate missing values between midnights
        """

        steps = int(self.interpolate_steps)

        if steps > 1440:
            raise ValueError('Max number of steps is 1440')

        dates = []
        moods = []
        step = 1440//steps  # Step size in minutes

        for i in range(len(self.__avg_moods)):  # pylint: disable=consider-using-enumerate
            current_point = self.__avg_moods[i]

            try:
                next_point = self.__avg_moods[i + 1]
            except IndexError:
                # Add last day as the date on midnight
                next_time = datetime.time(hour=0, minute=0)
                next_dt = current_point[0].combine(current_point[0], next_time)

                dates.append(next_dt)
                moods.append(current_point[1])

                break

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

        self.__dates = np.array(dates)
        self.__moods = np.array(moods)

    def __split_into_bands(self):
        for mood_name, boundaries in config.BOUNDARIES.items():
            # boundaries is a tuple of (low, high)
            # Upper bound
            masked_data = np.ma.masked_where(self.__moods >= boundaries[1], self.__moods)

            # Lower bound -- already working with partly masked data
            masked_data = np.ma.masked_where(self.__moods < boundaries[0], masked_data)

            self.__masked_data[mood_name] = masked_data

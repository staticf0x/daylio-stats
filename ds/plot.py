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
        self.rolling_window_size = 10  # Rolling mean window size

    def plot_average_moods(self, output_name=None):
        """
        Plot the average mood data into a PNG file
        """

        if not output_name:
            output_name = 'daylio-plot-{}.png'.format(time.strftime('%Y-%m-%d-%H%M%S'))

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

        print('Plotting mood chart...')

        dates, masked_data = self.__plot_data(self.__avg_moods)
        plot_args = self.__plot_args(dates, masked_data)

        ax1.plot(*plot_args)
        ax1.set_title('Average mood in each day')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Mood')
        ax1.set_yticks(np.arange(1, len(config.MOODS) + 1, 1))
        ax1.grid()

        print('Plotting rolling average chart...')

        dates, masked_data = self.__plot_data(self.__rolling_mean(self.__avg_moods))
        plot_args = self.__plot_args(dates, masked_data)

        ax2.plot(*plot_args)
        ax2.set_title(f'Rolling average of moods, window size = {self.rolling_window_size}')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Mood')
        ax2.set_yticks(np.arange(1, len(config.MOODS) + 1, 1))
        ax2.grid()

        print(f'Chart saved to: {output_name}')

        plt.tight_layout()
        plt.savefig(output_name, dpi=120)

    def __plot_args(self, dates, masked_data):
        plot_args = []

        for mood_name, color in config.COLORS.items():
            plot_args.append(dates)
            plot_args.append(masked_data[mood_name])
            plot_args.append(color)

        return plot_args

    def __plot_data(self, source_data):
        dates, moods = self.__interpolate(source_data)
        split_data = self.__split_into_bands(moods)

        return dates, split_data

    def __interpolate(self, avg_moods):
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

        return np.array(dates), np.array(moods)

    def __split_into_bands(self, moods):
        split_data = dict.fromkeys(config.BOUNDARIES.keys())

        for mood_name, boundaries in config.BOUNDARIES.items():
            # boundaries is a tuple of (low, high)
            # Upper bound
            masked_data = np.ma.masked_where(moods >= boundaries[1], moods)

            # Lower bound -- already working with partly masked data
            masked_data = np.ma.masked_where(moods < boundaries[0], masked_data)

            split_data[mood_name] = masked_data

        return split_data

    def __rolling_mean(self, source_data):
        N = self.rolling_window_size
        data = np.array(source_data)

        # Compute the rolling mean for our data
        # Moods are stored in the 1st column, dates in 0th
        filtered_data = np.convolve(data[:, 1], np.ones((N, ))/N, mode='valid')

        # Fill the missing entries with NaN,
        # so we can replace the original column
        # with filtered data
        nans = np.zeros(N - 1)
        nans[:] = np.nan
        filtered_data = np.concatenate((nans, filtered_data))
        data[:, 1] = filtered_data

        return data

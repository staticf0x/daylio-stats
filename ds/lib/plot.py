# -*- coding: utf-8 -*-
"""
A class for plotting the data
"""

import io
import datetime
import numpy as np
import matplotlib.pyplot as plt
from ds.lib import config
from ds.lib.stats import Stats


class Plot:
    """
    A class for interpolating and plotting the data
    """

    def __init__(self, avg_moods, plots=(5, )):
        self.__avg_moods = avg_moods
        self.plots = plots
        self.stats = Stats(avg_moods)

    def plot_average_moods(self, output_name=None):
        """
        Plot the average mood data into a PNG file.
        If output_name is not provided, returns a buffer
        with the image data. Otherwise returns the output_name.

        TODO: Might not be a good idea to return two different things
        """

        count_plots = 1 + len(self.plots)

        fig, axes = plt.subplots(count_plots,
                                 1,
                                 figsize=(12, 4*count_plots))

        dates, masked_data = self.__plot_data(self.__avg_moods)
        plot_args = self.__plot_args(dates, masked_data)

        axes[0].plot(*plot_args)
        axes[0].set_title('Average mood in each day')
        axes[0].set_xlabel('Date')
        axes[0].set_ylabel('Mood')
        axes[0].set_yticks(np.arange(1, len(config.MOODS) + 1, 1))
        axes[0].grid()

        self.__plot_rolling_means(axes[1:])

        plt.tight_layout()

        if output_name:
            fwrite = output_name
        else:
            fwrite = io.BytesIO()

        plt.savefig(fwrite, dpi=120)

        if not output_name:
            fwrite.seek(0)

        return fwrite

    def __plot_rolling_means(self, axes):
        for i, n in enumerate(self.plots):
            dates, masked_data = self.__plot_data(self.stats.rolling_mean(n))
            plot_args = self.__plot_args(dates, masked_data)

            axes[i].plot(*plot_args)
            axes[i].set_title(f'Rolling average of moods, window size = {n}')
            axes[i].set_xlabel('Date')
            axes[i].set_ylabel('Mood')
            axes[i].set_yticks(np.arange(1, len(config.MOODS) + 1, 1))
            axes[i].grid()

    def __plot_args(self, dates, masked_data):
        plot_args = []

        for mood_name, color in config.COLORS.items():
            plot_args.append(dates)
            plot_args.append(masked_data[mood_name])
            plot_args.append(color)

        return plot_args

    def __plot_data(self, source_data):
        dates, moods = self.stats.interpolate(source_data)
        split_data = self.stats.split_into_bands(moods)

        return dates, split_data

# -*- coding: utf-8 -*-
"""
A class for plotting the data
"""

import io
from typing import List

import matplotlib.pyplot as plt
import numpy as np
from daylio_parser.config import MoodConfig
from daylio_parser.parser import Entry
from daylio_parser.plot import PlotData
from daylio_parser.stats import Stats


class Plot:
    """
    A class for interpolating and plotting the data
    """

    def __init__(self, entries: List[Entry], plots=(5, )):
        self.entries = entries
        self.plots = plots

        self.config = MoodConfig()
        self.stats = Stats(entries, self.config)
        self.plotdata = PlotData(entries, self.config)

    def plot_average_moods(self, output_name=None):
        """
        Plot the average mood data into a PNG file.
        If output_name is not provided, returns a buffer
        with the image data. Otherwise returns the output_name.

        TODO: Might not be a good idea to return two different things
        """

        count_plots = 1 + len(self.plots)

        _, axes = plt.subplots(count_plots,
                               1,
                               figsize=(12, 4*count_plots))

        dates, masked_data = self.__plot_data()
        plot_args = self.__plot_args(dates, masked_data)

        axes[0].plot(*plot_args)
        axes[0].set_title('Average mood in each day')
        axes[0].set_xlabel('Date')
        axes[0].set_ylabel('Mood')
        axes[0].set_yticks(np.arange(1, len(self.config.moods) + 1, 1))
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
            axes[i].set_yticks(np.arange(1, len(self.config.moods) + 1, 1))
            axes[i].grid()

    def __plot_args(self, dates, masked_data):
        plot_args = []

        # Quick dirty "optimization"
        # TODO: Make this better
        # Added max() because of issue #9
        n = max(1, int(len(dates)//40e3))

        dates = dates[::n]

        for mood in self.config.moods:
            masked_data[mood.name] = masked_data[mood.name][::n]

            plot_args.append(dates)
            plot_args.append(masked_data[mood.name])
            plot_args.append(mood.color)

        return plot_args

    def __plot_data(self, data=None):
        dates, moods = self.plotdata.interpolate(data)
        split_data = self.plotdata.split_into_bands(moods)

        return dates, split_data

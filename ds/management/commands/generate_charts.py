#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A command to load the data and plot them manually
"""

import time
from django.core.management.base import BaseCommand
import ds.lib


class Command(BaseCommand):
    help = 'Generate the charts manually'

    def add_arguments(self, parser):
        DEFAULT_OUTPUT_NAME = 'daylio-plot-{}.png'.format(time.strftime('%Y-%m-%d-%H%M%S'))

        parser.add_argument('path', type=str, help='Path to the Daylio export')
        parser.add_argument('--output', '-o', type=str, default=DEFAULT_OUTPUT_NAME,
                            help='Ouptut path for the plot')

    def handle(self, *args, **kwargs):
        # TODO: Check that the path exists
        print('Loading data...')

        loader = ds.lib.data.DataLoader(kwargs['path'])
        loader.load()

        plots = (5, 10)

        print('Generating charts...')
        plot = ds.lib.plot.Plot(loader.avg_moods, plots)
        plot.plot_average_moods(kwargs['output'])

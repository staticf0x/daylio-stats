#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A command to load the data and plot them manually
"""

import json
import os
import time

from daylio_parser.config import MoodConfig
from daylio_parser.parser import Parser
from django.core.management.base import BaseCommand

import ds.lib


class Command(BaseCommand):
    help = 'Generate the charts manually'

    def add_arguments(self, parser):
        DEFAULT_OUTPUT_NAME = 'daylio-plot-{}.png'.format(time.strftime('%Y-%m-%d-%H%M%S'))

        parser.add_argument('path', type=str, help='Path to the Daylio export')
        parser.add_argument(
            '--output', '-o', type=str, default=DEFAULT_OUTPUT_NAME, help='Ouptut path for the plot'
        )
        parser.add_argument('--config', '-c', type=str, help='Path to the config file')

    def handle(self, *args, **kwargs):
        if not os.path.exists(kwargs['path']):
            print(f'Path: {kwargs["path"]} doesn\'t exist')
            return

        print('Loading config...')

        if kwargs['config']:
            if not os.path.exists(kwargs['config']):
                print(f'Config file: {kwargs["config"]} doesn\'t exist')
                return

            with open(kwargs['config'], 'r') as fread:
                data = json.load(fread)

                moods = data.get('moods')
                colors = data.get('colors')

                config = MoodConfig(moods, colors)
        else:
            config = MoodConfig()

        print('Loading data...')

        parser = Parser(config)
        entries = parser.load_csv(kwargs['path'])

        plots = (5, 10)

        print('Generating charts...')
        plot = ds.lib.plot.Plot(entries, plots)
        plot.plot_average_moods(kwargs['output'])

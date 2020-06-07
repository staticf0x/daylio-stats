#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

from django.core.management.base import BaseCommand
import ds.lib
import numpy as np


class Command(BaseCommand):
    help = 'Generate additional stats'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='Path to the Daylio export')

    def handle(self, *args, **kwargs):
        # Load the data
        loader = ds.lib.data.DataLoader(kwargs['path'])
        loader.load()

        avg_moods = np.array(loader.avg_moods)

        stats = ds.lib.stats.Stats(loader.avg_moods)

        mean, std = stats.mean()

        print(f'Average mood: {mean:.2f} ± {std:.2f}')
        print()

        print('Highs:')
        for period in stats.find_high_periods():
            print('{} — {}, {:2d} days, avg: {:.2f}'.format(period.start_date.strftime('%d/%m/%Y'),
                                                            period.end_date.strftime('%d/%m/%Y'),
                                                            period.duration,
                                                            period.avg_mood))

        print('\nLows:')
        for period in stats.find_low_periods():
            print('{} — {}, {:2d} days, avg: {:.2f}'.format(period.start_date.strftime('%d/%m/%Y'),
                                                            period.end_date.strftime('%d/%m/%Y'),
                                                            period.duration,
                                                            period.avg_mood))

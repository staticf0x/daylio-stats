#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Look for high and low periods in the data
"""

import datetime
import os

import numpy as np
from django.core.management.base import BaseCommand

from daylio_parser.parser import Parser
from daylio_parser.stats import Stats

OUTPUT_FMT = '{} — {}, {:2d} days, avg: {:.2f}{}'


class Command(BaseCommand):
    help = 'Generate additional stats'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='Path to the Daylio export')

    def handle(self, *args, **kwargs):
        if not os.path.exists(kwargs['path']):
            print(f'Path: {kwargs["path"]} doesn\'t exist')
            return

        # Load the data
        parser = Parser()
        entries = parser.load_csv(kwargs['path'])

        stats = Stats(entries)

        mean, std = stats.mean()

        print(f'Average mood: {mean:.2f} ± {std:.2f}')
        print()

        today = datetime.datetime.now().date()

        print('Highs:')
        for period in stats.find_high_periods():
            until_today = today - period.end_date
            recent = ''

            if until_today.days < 14:
                recent = f' ({until_today.days} days ago)'

            print(OUTPUT_FMT.format(period.start_date.strftime('%d/%m/%Y'),
                                    period.end_date.strftime('%d/%m/%Y'),
                                    period.duration,
                                    period.avg_mood,
                                    recent))

        print('\nLows:')
        for period in stats.find_low_periods():
            until_today = today - period.end_date
            recent = ''

            if until_today.days < 14:
                recent = f' ({until_today.days} days ago)'

            print(OUTPUT_FMT.format(period.start_date.strftime('%d/%m/%Y'),
                                    period.end_date.strftime('%d/%m/%Y'),
                                    period.duration,
                                    period.avg_mood,
                                    recent))

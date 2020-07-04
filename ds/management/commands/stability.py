#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Look at how much the mood changes over one day
"""

import datetime
from collections import Counter

import numpy as np
from django.core.management.base import BaseCommand

import ds.lib


def stability(x):
    """
    Compute mood stability for an input of mood count.

    For example:
        Mood count in a day: [ 1,  2,  3, 4, 5]
        Input:               [50, 20, 10, 2, 1]
        Output:              84.94%
    """

    return (1*x[0] + .75*x[1] + .5*x[2] + .25*x[3] + 0*x[4])/sum(x)


class Command(BaseCommand):
    help = 'Generate additional stats'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='Path to the Daylio export')

    def handle(self, *args, **kwargs):
        # Load the data
        loader = ds.lib.data.DataLoader(kwargs['path'])
        loader.load()

        group_by_date = loader.get_raw_data()

        # Count number of moods per date
        count_by_date = {}

        for date_str, moods in group_by_date.items():
            count_by_date[date_str] = len(Counter(moods))

        # Total days in the export
        total_days = len(count_by_date)

        # Count the days where N number of moods occur
        mood_counts = Counter(count_by_date.values())
        mood_counts_list = [0, 0, 0, 0, 0]

        print('Mood count   Days   Days/Total days')

        for mood_count, count in sorted(mood_counts.items()):
            perc = count/total_days
            mood_counts_list[mood_count - 1] = count

            print(f'{mood_count}            {count:4d}   {perc:6.2%}')

        # Calculate mood stability
        mood_stability = stability(mood_counts_list)

        print()
        print(f'Stability: {mood_stability:.2%}')

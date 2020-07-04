#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Show a list of activities from best to worst
"""

import numpy as np
from django.core.management.base import BaseCommand

import ds.lib


class Command(BaseCommand):
    help = 'Generate additional stats'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='Path to the Daylio export')

    def handle(self, *args, **kwargs):
        # Load the data
        loader = ds.lib.data.DataLoader(kwargs['path'])
        loader.load()

        activities_moods = {}

        for entry in loader.entries:
            for activity in entry.activities:
                activities_moods.setdefault(activity, [])
                activities_moods[activity].append(entry.mood)

        activities_avg = {}

        for activity, moods in activities_moods.items():
            activities_avg[activity] = (np.mean(moods), np.std(moods))

        for activity, data in sorted(activities_avg.items(), key=lambda x: x[1][0], reverse=True):
            print(f'{activity:15s} {data[0]:.2f} ± {data[1]:.2f}')

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Show a list of activities from best to worst
"""

import os

import numpy as np
from daylio_parser.parser import Parser
from daylio_parser.stats import Stats
from django.core.management.base import BaseCommand


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
        activities_avg = stats.activity_moods()

        for activity, data in sorted(activities_avg.items(), key=lambda x: x[1][0], reverse=True):
            print(f'{activity:15s} {data[0]:.2f} ± {data[1]:.2f}')

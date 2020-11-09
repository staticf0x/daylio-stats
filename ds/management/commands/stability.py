#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Look at how much the mood changes over one day
"""

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

        stability = ds.lib.stability.Stability(loader)
        stability.stability_plot()

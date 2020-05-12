#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main file to load the data and plot them
"""

import argparse
import time
import ds

DEFAULT_OUTPUT_NAME = 'daylio-plot-{}.png'.format(time.strftime('%Y-%m-%d-%H%M%S'))

parser = argparse.ArgumentParser()
parser.add_argument('path', type=str, help='Path to the Dailyo export')
parser.add_argument('--output', '-o', type=str, default=DEFAULT_OUTPUT_NAME,
                    help='Ouptut path for the plot')

args = parser.parse_args()

loader = ds.data.DataLoader(args.path)
avg_moods = loader.load()

plot = ds.plot.Plot(avg_moods)
plot.plot_average_moods(args.output)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main file to read the CSV and save a plot
"""

import argparse
import csv
import time
import datetime
import matplotlib.pyplot as plt
import numpy as np

DEFAULT_OUTPUT_NAME = 'daylio-plot-{}.png'.format(time.strftime('%Y-%m-%d-%H%M%S'))

parser = argparse.ArgumentParser()
parser.add_argument('path', type=str, help='Path to the Dailyo export')
parser.add_argument('--output', '-o', type=str, default=DEFAULT_OUTPUT_NAME,
                    help='Ouptut path for the plot')

args = parser.parse_args()

MOODS = {
    'awful': 1,
    'bad': 2,
    'meh': 3,
    'good': 4,
    'rad': 5
}

BOUNDARIES = {
    'awful': (1, 1.5),
    'bad': (1.5, 2.5),
    'meh': (2.5, 3.5),
    'good': (3.5, 4.5),
    'rad': (4.5, 5)
}


def read_raw_moods(path):
    """
    Read mood data from CSV file
    """

    data_tmp = {}

    with open(path) as fread:
        csv_reader = csv.reader(fread, delimiter=',', quotechar='"')
        next(csv_reader)  # Skip header

        for row in csv_reader:
            date = row[0]
            mood_str = row[4]
            mood = MOODS[mood_str]

            data_tmp.setdefault(date, [])
            data_tmp[date].append(mood)

    return data_tmp


def get_avg_moods(data_tmp):
    """
    Go through the raw data (date: mood list) and compute average
    values for each day
    """

    data = []

    for date, moods_raw in data_tmp.items():
        dt = datetime.datetime.strptime(date, '%Y-%m-%d')
        mood_avg = np.mean(moods_raw)

        data.append((dt, mood_avg))

    data.reverse()

    return data


def interpolate(data, steps=24):
    """
    Interpolate missing values between midnights
    """

    steps = int(steps)

    if steps > 1440:
        raise ValueError('Max number of steps is 1440')

    dates = []
    moods = []
    step = 1440//steps  # Step size in minutes

    for i in range(len(data)):  # pylint: disable=consider-using-enumerate
        current_point = data[i]

        try:
            next_point = data[i + 1]
        except IndexError:
            # Add last day as the date on midnight
            next_time = datetime.time(hour=0, minute=0)
            next_dt = current_point[0].combine(current_point[0], next_time)

            dates.append(next_dt)
            moods.append(current_point[1])

            break

        value_diff = next_point[1] - current_point[1]  # Mood difference between days
        time_diff = steps  # Time difference a.k.a. number of buckets
        coef = value_diff/time_diff  # How much the mood changes in one step

        for step_n in range(0, steps):
            # Simple linear interpolation
            next_value = step_n*coef + current_point[1]

            # step*step_n == number of minutes in the current day
            # just split it into hours and minutes for time object
            hour = 0 if step_n == 0 else (step*step_n)//60
            minute = 0 if step_n == 0 else (step*step_n)%60

            next_time = datetime.time(hour=int(hour), minute=int(minute))
            next_dt = current_point[0].combine(current_point[0], next_time)

            dates.append(next_dt)
            moods.append(next_value)

    dates = np.array(dates)
    moods = np.array(moods)

    return dates, moods


data_tmp = read_raw_moods(args.path)
data = get_avg_moods(data_tmp)
dates, moods = interpolate(data, 1440//2)

# Split moods into sections

# Awful
m_awful = np.ma.masked_where(moods >= BOUNDARIES['awful'][1], moods)
m_awful = np.ma.masked_where(moods < BOUNDARIES['awful'][0], m_awful)

# Bad
m_bad = np.ma.masked_where(moods >= BOUNDARIES['bad'][1], moods)
m_bad = np.ma.masked_where(moods < BOUNDARIES['bad'][0], m_bad)

# Meh
m_meh = np.ma.masked_where(moods >= BOUNDARIES['meh'][1], moods)
m_meh = np.ma.masked_where(moods < BOUNDARIES['meh'][0], m_meh)

# Good
m_good = np.ma.masked_where(moods >= BOUNDARIES['good'][1], moods)
m_good = np.ma.masked_where(moods < BOUNDARIES['good'][0], m_good)

# Rad
m_rad = np.ma.masked_where(moods >= BOUNDARIES['rad'][1], moods)
m_rad = np.ma.masked_where(moods < BOUNDARIES['rad'][0], moods)

fig, ax = plt.subplots(1, 1, figsize=(12, 4))

ax.plot(
    dates, m_awful, '#6C7679',
    dates, m_bad, '#5579A7',
    dates, m_meh, '#9454A3',
    dates, m_good, '#4CA369',
    dates, m_rad, '#FF8500',
)

# Misc
ax.set_xlabel('Date')
ax.set_ylabel('Mood')
ax.set_yticks(np.arange(1, 6, 1))
plt.grid()

# Show/save the plot
# plt.show()
plt.savefig(args.output, dpi=120)

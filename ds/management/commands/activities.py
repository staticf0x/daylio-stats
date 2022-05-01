"""Show a list of activities from best to worst."""

import json
import os

from daylio_parser.config import MoodConfig
from daylio_parser.parser import Parser
from daylio_parser.stats import Stats
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Command to display activity stats."""

    help = "Generate activity stats"

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument("path", type=str, help="Path to the Daylio export")
        parser.add_argument("--config", "-c", type=str, help="Path to the config file")

    def handle(self, *args, **kwargs):
        """Run the command."""
        if not os.path.exists(kwargs["path"]):
            print(f'Path: {kwargs["path"]} doesn\'t exist')
            return

        if kwargs["config"]:
            if not os.path.exists(kwargs["config"]):
                print(f'Config file: {kwargs["config"]} doesn\'t exist')
                return

            with open(kwargs["config"], "r") as fread:
                data = json.load(fread)

                moods = data.get("moods")
                colors = data.get("colors")

                config = MoodConfig(moods, colors)
        else:
            config = MoodConfig()

        # Load the data
        parser = Parser(config)
        entries = parser.load_csv(kwargs["path"])

        stats = Stats(entries)
        activities_avg = stats.activity_moods()

        # TODO: Add coloring for different levels
        for activity, data in sorted(activities_avg.items(), key=lambda x: x[1][0], reverse=True):
            print(f"{activity:15s} {data[0]:.2f} ± {data[1]:.2f}")

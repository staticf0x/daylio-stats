"""Look for high and low periods in the data."""

import datetime
import json
import os

from daylio_parser.config import MoodConfig
from daylio_parser.parser import Parser
from daylio_parser.stats import Stats
from django.core.management.base import BaseCommand

OUTPUT_FMT = "{} — {}, {:2d} days, avg: {:.2f}{}"


class Command(BaseCommand):
    """Command to generate additional stats."""

    help = "Generate additional stats"

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

        stats = Stats(entries, config)

        mean, std = stats.mean()

        print(f"Average mood: {mean:.2f} ± {std:.2f}")
        print()

        today = datetime.datetime.now().date()

        print("Highs:")
        for period in stats.find_high_periods():
            until_today = today - period.end_date
            recent = ""

            if until_today.days < 14:
                recent = f" ({until_today.days} days ago)"

            print(
                OUTPUT_FMT.format(
                    period.start_date.strftime("%d/%m/%Y"),
                    period.end_date.strftime("%d/%m/%Y"),
                    period.duration,
                    period.avg_mood,
                    recent,
                )
            )

        print("\nLows:")
        for period in stats.find_low_periods():
            until_today = today - period.end_date
            recent = ""

            if until_today.days < 14:
                recent = f" ({until_today.days} days ago)"

            print(
                OUTPUT_FMT.format(
                    period.start_date.strftime("%d/%m/%Y"),
                    period.end_date.strftime("%d/%m/%Y"),
                    period.duration,
                    period.avg_mood,
                    recent,
                )
            )

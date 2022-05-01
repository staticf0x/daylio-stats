"""Look at how much the mood changes over one day."""

import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generate additional stats"

    def add_arguments(self, parser):
        parser.add_argument("path", type=str, help="Path to the Daylio export")

    def handle(self, *args, **kwargs):
        if not os.path.exists(kwargs["path"]):
            print(f'Path: {kwargs["path"]} doesn\'t exist')
            return

        raise NotImplementedError

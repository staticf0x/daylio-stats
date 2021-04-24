"""Endpoints for user data."""

from daylio_parser.plot import PlotData
from django.http import JsonResponse

from ds.lib import api_login_required
from ds.lib.data import get_user_mood_config
from ds.lib.entries import EntryConverter


@api_login_required
def moods(request):
    # TODO: These are dummy data
    data = {
        'status': 'ok',
        'data': {
            'labels': ['a', 'b', 'c'],
            'datasets': [
                {
                    'label': 'Mood',
                    'data': [1, 2, 1.5]
                }
            ]
        }
    }

    conv = EntryConverter(request.user)
    entries = conv.get_entries()
    mood_config = get_user_mood_config(request.user)

    plot_data = PlotData(entries, mood_config)

    # TODO: The rest

    return JsonResponse(data)

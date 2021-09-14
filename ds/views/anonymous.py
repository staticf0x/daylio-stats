"""Views for anonymous users."""

import time
import urllib

from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

import ds.lib


def process(request):
    """Process the input file and redirect to result page."""
    if not request.FILES.get('csv', None):
        params = {'err': 'no-input-file'}
        return redirect('{}?{}'.format(reverse('ds:index'), urllib.parse.urlencode(params)))

    entries = ds.lib.data.get_entries_from_upload(request.FILES['csv'])

    # Create the charts and save them into a buffer
    plot = ds.lib.plot.Plot(entries)
    buf = plot.plot_average_moods()

    # Send the buffer as an attachment to the client
    output_name = 'daylio-plot-{}.png'.format(time.strftime('%Y-%m-%d-%H%M%S'))

    response = HttpResponse(buf, content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename={output_name}'

    return response

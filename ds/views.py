# -*- coding: utf-8 -*-
"""
Project views
"""

import codecs
import io
import time
import urllib

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from daylio_parser.parser import Parser

import ds.lib


def index(request):
    """
    Main landing page
    """

    cont = {}

    return render(request, 'ds/index.html', cont)


def about(request):
    """
    About page with info about the project
    """

    return render(request, 'ds/about.html', {})


def contributing(request):
    """
    Info about contributing to the project
    """

    return render(request, 'ds/contributing.html', {})


def process(request):
    """
    Process the input file and redirect to result page
    """

    if not request.FILES.get('csv', None):
        params = {'err': 'no-input-file'}
        return redirect('{}?{}'.format(reverse('ds:index'), urllib.parse.urlencode(params)))

    # Write the uploaded file into a buffer
    buf = io.BytesIO()

    for chunk in request.FILES['csv'].chunks():
        buf.write(chunk)

    buf.seek(0)

    # Convert to StringIO so the CSV reader can iterate over strings and not bytes
    stream_reader = codecs.getreader('utf-8')
    wrapped_file = stream_reader(buf)

    # Load the CSV
    parser = Parser()
    entries = parser.load_from_buffer(wrapped_file)
    buf.close()

    # Create the charts and save them into a buffer
    plot = ds.lib.plot.Plot(entries)
    buf = plot.plot_average_moods()

    # Send the buffer as an attachment to the client
    output_name = 'daylio-plot-{}.png'.format(time.strftime('%Y-%m-%d-%H%M%S'))

    response = HttpResponse(buf, content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename={output_name}'

    return response

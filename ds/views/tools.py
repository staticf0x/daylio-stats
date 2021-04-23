"""Tools for logged-in users."""

import time

from daylio_parser.parser import Parser
from daylio_parser.stats import Stats
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

import ds.lib
from ds import models


@login_required(login_url='/login/')
def dashboard(request):
    """Main dashboard."""

    cont = {}

    entries = models.Entry.objects.filter(user=request.user).order_by('datetime')

    cont['count'] = entries.count()
    cont['first'] = entries[0]
    cont['last'] = entries[entries.count() - 1]
    cont['days_since_first'] = (cont['last'].datetime - cont['first'].datetime).days

    return render(request, 'ds/tools/dashboard.html', cont)


@login_required(login_url='/login/')
def upload(request):
    """View for uploading CSV files for a user."""

    cont = {}

    if request.method == 'POST':
        if not request.FILES.get('csv', None):
            params = {'err': 'no-input-file'}
            return redirect('{}?{}'.format(reverse('ds:upload'), urllib.parse.urlencode(params)))

        entries = ds.lib.data.get_entries_from_upload(request.FILES['csv'])

        user_import = ds.lib.data.UserDataImport(request.user)
        user_import.import_entries(entries)

        return redirect('ds:dashboard')

    return render(request, 'ds/tools/upload.html', cont)


@login_required(login_url='/login/')
def activities(request):
    """Overview of activities and their average moods."""

    cont = {}

    conv = ds.lib.entries.EntryConverter(request.user)
    entries = conv.get_entries()

    stats = Stats(entries, ds.lib.data.get_user_mood_config(request.user))

    cont['activities'] = sorted(stats.activity_moods().items(), key=lambda x: x[1], reverse=True)

    return render(request, 'ds/tools/activities.html', cont)


@login_required(login_url='/login/')
def export(request):
    """Export chart (similar to anonymous upload)."""

    cont = {}

    if request.method == 'POST' and request.POST.get('export') == '1':
        conv = ds.lib.entries.EntryConverter(request.user)
        entries = conv.get_entries()

        # Create the charts and save them into a buffer
        plot = ds.lib.plot.Plot(entries)
        buf = plot.plot_average_moods()

        # Send the buffer as an attachment to the client
        output_name = 'daylio-plot-{}.png'.format(time.strftime('%Y-%m-%d-%H%M%S'))

        response = HttpResponse(buf, content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename={output_name}'

        return response

    return render(request, 'ds/tools/export.html', cont)

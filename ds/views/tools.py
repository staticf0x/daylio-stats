"""Tools for logged-in users."""

from daylio_parser.parser import Parser
from django.contrib.auth.decorators import login_required
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

    conv = ds.lib.entries.EntryConverter(request.user)

    return render(request, 'ds/dashboard.html', cont)


@login_required(login_url='/login/')
def upload(request):
    cont = {}

    if request.method == 'POST':
        if not request.FILES.get('csv', None):
            params = {'err': 'no-input-file'}
            return redirect('{}?{}'.format(reverse('ds:upload'), urllib.parse.urlencode(params)))

        entries = ds.lib.data.get_entries_from_upload(request.FILES['csv'])

        user_import = ds.lib.data.UserDataImport(request.user)
        user_import.import_entries(entries)

        return redirect('ds:dashboard')

    return render(request, 'ds/upload.html', cont)

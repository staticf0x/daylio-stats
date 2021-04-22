# -*- coding: utf-8 -*-
"""
Project views
"""

import time
import urllib

from daylio_parser.parser import Parser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

import ds.forms
import ds.lib
from ds import models


def index(request):
    """
    Main landing page
    """

    cont = {}

    return render(request, 'ds/index.html', cont)


@login_required(login_url='/login/')
def dashboard(request):
    """
    Dashboard
    """

    cont = {}

    entries = models.Entry.objects.filter(user=request.user).order_by('datetime')

    cont['count'] = entries.count()
    cont['first'] = entries[0]
    cont['last'] = entries[entries.count() - 1]
    cont['days_since_first'] = (cont['last'].datetime - cont['first'].datetime).days

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


def about(request):
    """
    About page with info about the project
    """

    return render(request, 'ds/about.html', {})


def process(request):
    """
    Process the input file and redirect to result page
    """

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


def login_view(request):
    cont = {}

    # TODO: Check GET param 'next' for redirects
    if request.method == 'POST':
        login_form = ds.forms.LoginForm(request.POST)

        if login_form.is_valid():
            # User can log in
            user = authenticate(
                username=request.POST.get('username'),
                password=request.POST.get('password')
            )

            login(request, user)

            return redirect('ds:index')

        cont['form'] = login_form

    return render(request, 'ds/login.html', cont)


def logout_view(request):
    logout(request)

    return redirect('ds:index')


@login_required(login_url='/login/')
def settings(request):
    cont = {}

    settings = models.UserSettings.objects.get(user=request.user)
    settings_form = ds.forms.SettingsForm(request.POST or None, instance=settings)

    if request.method == 'POST':
        if settings_form.is_valid():
            settings_form.save()

            return redirect('ds:settings')

    cont['form'] = settings_form

    return render(request, 'ds/settings.html', cont)

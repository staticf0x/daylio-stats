"""User management views."""

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

import ds.forms
from ds import models


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

            return redirect('ds:dashboard')

        cont['form'] = login_form

    return render(request, 'ds/login.html', cont)


def logout_view(request):
    logout(request)

    return redirect('ds:index')


def register(request):
    """View for registering new accounts."""

    if request.user.is_authenticated:
        return redirect('ds:dashboard')

    cont = {}

    if request.method == 'POST':
        register_form = ds.forms.RegisterForm(request.POST)

        # TODO: Check for password complexity!
        if register_form.is_valid():
            # Create the user object
            user = User.objects.create_user(
                request.POST.get('username'),
                '',
                request.POST.get('password')
            )
            user.save()

            # Create default UserSettings
            user_settings = models.UserSettings()
            user_settings.user = user
            user_settings.save()

            # Login the new user
            user = authenticate(
                username=request.POST.get('username'),
                password=request.POST.get('password')
            )

            login(request, user)

            return redirect('ds:dashboard')

        cont['form'] = register_form

    return render(request, 'ds/register.html', cont)


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


@login_required(login_url='/login/')
def delete_account(request):
    if request.method == 'POST':
        # TODO: Delete account
        pass

    return redirect('ds:index')

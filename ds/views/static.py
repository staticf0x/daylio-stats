"""Static views."""

from django.shortcuts import render


def index(request):
    """Main landing page."""

    return render(request, 'ds/index.html', {})


def about(request):
    """About page with info about the project."""

    return render(request, 'ds/about.html', {})

"""Static views."""

from django.shortcuts import render


def index(request):
    """Render main landing page."""
    return render(request, 'ds/index.html', {})


def about(request):
    """Render about page with info about the project."""
    return render(request, 'ds/about.html', {})

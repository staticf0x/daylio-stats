from django.shortcuts import render
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

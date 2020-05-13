from django.shortcuts import render
import ds.lib


def index(request):
    cont = {}

    return render(request, 'ds/index.html', cont)

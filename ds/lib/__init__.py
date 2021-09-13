# -*- coding: utf-8 -*-
"""
Lib for the project
"""

from django.http import JsonResponse

from . import data, entries, plot


def api_login_required(view):
    """
    Decorator for requiring user login for API endpoints.
    Instead of redirecting to a login view, this will return
    a JSON object with an error:
    {
        "status": "error",
        "message": "..."
    }
    """

    def inner(request):
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'Not authenticated'}, status=403)

        return view(request)

    return inner

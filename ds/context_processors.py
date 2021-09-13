# -*- coding: utf-8 -*-
"""
Some global variables for templates
"""

VERSION = '0.0.1'

ERRORS = {
    'no-input-file': 'No input file',
}


def global_vars(request):
    """
    Add global variables
    """

    cont = {'VERSION': VERSION}

    if request.GET.get('err', None):
        cont['ERR'] = ERRORS.get(request.GET['err'], 'Unknown error')

    return cont

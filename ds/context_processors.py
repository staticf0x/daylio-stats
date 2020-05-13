# -*- coding: utf-8 -*-
"""
Some global variables for templates
"""

VERSION = '0.0.1'


def global_vars(request):
    """
    Add global variables
    """

    cont = {
        'VERSION': VERSION
    }

    return cont

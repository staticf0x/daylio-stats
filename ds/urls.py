# -*- coding: utf-8 -*-
"""
URL config for the ds (main) app
"""

from django.urls import path
from ds import views

urlpatterns = [
    path('', views.index, name='index'),
]

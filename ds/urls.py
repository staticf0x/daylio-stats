# -*- coding: utf-8 -*-
"""
URL config for the ds (main) app
"""

from django.urls import path
from ds import views

app_name = 'ds'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contributing/', views.contributing, name='contributing'),
]

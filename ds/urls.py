# -*- coding: utf-8 -*-
"""
URL config for the ds (main) app
"""

from django.urls import path

from ds import views

app_name = 'ds'

urlpatterns = [
    # Anonymous processing
    path('', views.index, name='index'),
    path('process/', views.process, name='process'),

    # For logged-in users
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload, name='upload'),
    path('settings/', views.settings, name='settings'),
    path('settings/delete/', views.delete_account, name='delete_account'),

    # Static pages
    path('about/', views.about, name='about'),

    # Login/logout
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

# -*- coding: utf-8 -*-
"""
URL config for the ds (main) app
"""

from django.urls import path

from ds import views

app_name = 'ds'

urlpatterns = [
    # Static pages
    path('', views.static.index, name='index'),
    path('about/', views.static.about, name='about'),

    # Anonymous processing
    path('process/', views.anonymous.process, name='process'),

    # Tools for logged-in users
    path('dashboard/', views.tools.dashboard, name='dashboard'),
    path('upload/', views.tools.upload, name='upload'),
    path('activities/', views.tools.activities, name='activities'),
    path('export/', views.tools.export, name='export'),

    # User views
    path('settings/', views.users.settings, name='settings'),
    path('settings/delete/', views.users.delete_account, name='delete_account'),
    path('login/', views.users.login_view, name='login'),
    path('logout/', views.users.logout_view, name='logout'),
]

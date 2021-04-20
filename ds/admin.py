"""
Admin model registration
"""

from django.contrib import admin

from ds import models

admin.site.register(models.UserSettings)
admin.site.register(models.Activity)
admin.site.register(models.Entry)

# -*- coding: utf-8 -*-
"""
Forms
"""

from django import forms
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(max_length=150, required=True)

    def clean(self):
        super().clean()

        user = authenticate(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )

        if not user:
            raise forms.ValidationError('Username or password incorrect')

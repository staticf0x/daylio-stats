"""Project forms."""

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from ds.models import UserSettings


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(max_length=150, required=True)

    def clean(self):
        super().clean()

        user = authenticate(
            username=self.cleaned_data['username'], password=self.cleaned_data['password']
        )

        if not user:
            raise forms.ValidationError('Username or password incorrect')


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(max_length=150, required=True)
    password_confirm = forms.CharField(max_length=150, required=True)

    def clean_password_confirm(self):
        """Check if passwords match."""
        if 'password' in self.cleaned_data and 'password_confirm' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['password_confirm']:
                raise forms.ValidationError('Passwords don\'t match')

    def clean_username(self):
        """Check if user already exists."""
        try:
            _ = User.objects.get(username=self.cleaned_data['username'])

            raise forms.ValidationError('Username already exists')
        except User.DoesNotExist:
            return self.cleaned_data['username']


class SettingsForm(forms.ModelForm):
    class Meta:
        model = UserSettings
        fields = [
            'save_notes',
        ]

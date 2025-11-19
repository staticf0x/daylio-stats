"""Project forms."""

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from ds.models import UserSettings


class LoginForm(forms.Form):
    """Form for logging in."""

    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(max_length=150, required=True)

    def clean(self):
        """Authenticate the user. Raise ValidationError if the user doesn't exist."""
        super().clean()

        user = authenticate(
            username=self.cleaned_data["username"], password=self.cleaned_data["password"]
        )

        if not user:
            raise forms.ValidationError("Username or password incorrect")


class RegisterForm(forms.Form):
    """Registration form."""

    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(max_length=150, required=True)
    password_confirm = forms.CharField(max_length=150, required=True)

    def clean_password_confirm(self):
        """Check if passwords match."""
        if "password" in self.cleaned_data and "password_confirm" in self.cleaned_data:
            if self.cleaned_data["password"] != self.cleaned_data["password_confirm"]:
                raise forms.ValidationError("Passwords don't match")

    def clean_username(self):
        """Check if user already exists."""
        try:
            _ = User.objects.get(username=self.cleaned_data["username"])

            raise forms.ValidationError("Username already exists")
        except User.DoesNotExist:
            return self.cleaned_data["username"]


class SettingsForm(forms.ModelForm):
    """Form to modify UserSettings."""

    save_notes = forms.BooleanField()

    class Meta:  # noqa: D106
        model = UserSettings

        fields = [
            "save_notes",
        ]

    def __init__(self, *args, **kwargs):  # noqa: D107
        super().__init__(*args, **kwargs)

        settings = self.instance

        for i, (level, name) in enumerate(settings.mood_config):
            field_name_name = f"mood_{i}_name"
            field_name_value = f"mood_{i}_value"

            self.initial[field_name_name] = name
            self.initial[field_name_value] = level

            self.fields[field_name_name] = forms.CharField(max_length=32)
            self.fields[field_name_value] = forms.IntegerField(min_value=1, max_value=5)

    def get_mood_fields(self):
        """Get all the mood field in the format (idx, mood_name, mood_level)."""
        name_fields = [field for field in self.fields if field.endswith("_name")]
        value_fields = [field for field in self.fields if field.endswith("_value")]

        for i, (name_field, value_field) in enumerate(zip(name_fields, value_fields)):
            yield i, self.initial[name_field], self.initial[value_field]

    def clean(self):
        """Validate the data."""
        name_fields = [field for field in self.data if field.endswith("_name")]
        value_fields = [field for field in self.data if field.endswith("_value")]

        for name_field, value_field in zip(name_fields, value_fields):
            name = self.data[name_field]
            value = self.data[value_field]

            try:
                value = int(value)
            except TypeError:
                raise forms.ValidationError(f"{value_field} is not an integer")

            self.cleaned_data[name_field] = name
            self.cleaned_data[value_field] = value

    def save(self):
        """Save the form."""
        self.instance.save_notes = self.cleaned_data["save_notes"]

        name_fields = [field for field in self.cleaned_data if field.endswith("_name")]
        value_fields = [field for field in self.cleaned_data if field.endswith("_value")]

        moods = []

        for name_field, value_field in zip(name_fields, value_fields):
            name = self.cleaned_data[name_field]
            value = self.cleaned_data[value_field]

            moods.append([value, name])

        moods = sorted(moods, key=lambda x: x[0])
        self.instance.mood_config = moods

        self.instance.save()

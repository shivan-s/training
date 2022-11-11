"""Forms associated with the Profile model."""

from django import forms

from project.models import Profile

from .base import BaseCustomForm


class ProfileUpdateForm(BaseCustomForm, forms.ModelForm):
    """Provide update form for user profile."""

    def __init__(self, *args, **kwargs):
        """Overwrite `__init__`."""
        super().__init__(*args, **kwargs)

    class Meta:
        """Options."""

        model = Profile
        fields = ("name", "avatar")

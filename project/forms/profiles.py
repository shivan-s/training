"""Forms associated with the Profile model."""

from django import forms
from django.contrib.auth import get_user_model

from .base import BaseCustomForm

User = get_user_model()


class ProfileUpdateForm(BaseCustomForm, forms.ModelForm):
    """Provide update form for user profile."""

    def __init__(self, *args, **kwargs):
        """Overwrite `__init__`."""
        super().__init__(*args, **kwargs)
        self.fields["is_private"].widget.attrs.update({"class": "radio"})

    class Meta:
        """Options."""

        model = User
        fields = ("name", "avatar", "is_private")

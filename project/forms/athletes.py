"""Athlete forms."""

from django import forms

from .base import BaseCustomForm


class AthleteAddForm(BaseCustomForm, forms.Form):
    """Form used for coaches to add athlete by email."""

    email = forms.EmailField(label="Athlete Email")

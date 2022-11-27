"""Confirm Athlete view."""

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, reverse
from django.views.generic import View

from project.models import Athlete, Coach


class ConfirmAthleteForm(forms.Form):
    """Confirm athlete."""

    athlete = forms.CharField()


class ConfirmAthleteView(LoginRequiredMixin, View):
    """Confirm Athlete.

    The Coach confirms connecting with the athlete.
    """

    def post(self, request, *args, **kwargs):
        """Changing the post request."""
        form = ConfirmAthleteForm(request.POST)
        coach = Coach.objects.get(profile__user=request.user)
        if form.is_valid():
            athlete_pk = form.cleaned_data.get("athlete")
            athlete = Athlete.objects.get(profile__user__pk=athlete_pk)
            coach.athletes.add(athlete)
            athlete.coaches.add(coach)
            context = {"confirmed": True}
            return render(
                request,
                "coaches/add_athlete.html",
                context,
            )

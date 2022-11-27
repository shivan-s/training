"""Athlete views."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView, ListView, View

from project.models import Athlete


class AthleteListView(LoginRequiredMixin, ListView):
    """Athlete List view."""

    model = Athlete
    template_name = "athletes/list.html"
    paginate_by = 20


class AthleteDetailView(LoginRequiredMixin, DetailView):
    """Athlete Detail view."""

    model = Athlete
    template_name = "athletes/detail.html"

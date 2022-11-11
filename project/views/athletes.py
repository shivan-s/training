"""Athlete views."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView, View

from project.forms import AthleteAddForm
from project.models import Athlete


class AthleteAddView(LoginRequiredMixin, View):
    """Add an Athlete by email address."""

    form_class = AthleteAddForm
    template_name = "athletes/add.html"
    initial = {"email": "value"}

    def get(self, request, *args, **kwargs):
        """Get request."""
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"form ": form})

    def post(self, request, *args, **kwargs):
        """Post to handle email addresses."""
        form = self.form_class(request.POST)
        if form.is_valid():
            pass


class AthleteListView(LoginRequiredMixin, ListView):
    """Athlete List view."""

    model = Athlete
    template_name = "athletes/list.html"
    paginate_by = 20


class AthleteDetailView(LoginRequiredMixin, DetailView):
    """Athlete Detail view."""

    model = Athlete
    template_name = "athletes/detail.html"


class YourTrainingView(LoginRequiredMixin, TemplateView):

    template_name = "athlete/your_training.html"

    def get_context_data(self, *args, **kwargs):
        """Adding context data."""
        context = super().get_context_data(*args, **kwargs)
        return context

"""Coach views."""

from allauth.account.models import EmailAddress
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from project.forms.base import BaseCustomForm
from project.models import Athlete, Coach


class CoachPortalForm(BaseCustomForm, forms.Form):
    """Form for CoachPortalView.

    Field used to add an athlete by email address.
    """

    search = forms.CharField(label="", required=False)

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)
        self.fields["search"].widget.attrs["class"] = "input"
        self.fields["search"].widget.attrs["placeholder"] = "Filter athletes"


class CoachPortalView(LoginRequiredMixin, TemplateView):
    """Index view."""

    template_name = "coaches/portal.html"

    def post(self, request, *args, **kwargs):
        """Search an athlete."""
        form = CoachPortalForm(request.POST)
        coach = Coach.objects.get(user=request.user)
        context = {
            "form": form,
            "coach": coach,
        }
        if form.is_valid():
            q = form.cleaned_data.get("search")
            athletes = coach.athletes.filter(user__name__icontains=q)
            context["athletes"] = athletes
        return render(request, self.template_name, context)

    def get_context_data(self, *args, **kwargs):
        """Adding context data."""
        context = super().get_context_data(*args, **kwargs)
        context["form"] = CoachPortalForm
        context["coach"] = Coach.objects.get(user=self.request.user)
        # TODO: filter by last program?
        # context["athletes"] = context["coach"].athletes.order_by(
        #     "-programming_session__history__recent__date"
        # )
        context["athletes"] = context["coach"].athletes.all()
        return context

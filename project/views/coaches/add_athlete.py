"""Add Athlete view."""

from allauth.account.models import EmailAddress
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from project.forms.base import BaseCustomForm
from project.models import Athlete, Coach


class AddAthleteForm(BaseCustomForm, forms.Form):
    """Form for CoachPortalView.

    Field used to add an athlete by email address.
    """

    email = forms.EmailField(
        label="Add Athlete",
    )

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs[
            "placeholder"
        ] = "Enter athlete's email"

    def clean_email(self, *args, **kwargs):
        """Clean.

        1. Determine if the email exists on the database.
        """
        email = self.cleaned_data.get("email")
        if not EmailAddress.objects.filter(email=email).exists():
            raise ValidationError(
                _("No athlete found with this email."),
                code="no-email-found",
            )
        return email


class AddAthleteView(LoginRequiredMixin, TemplateView):
    """Index view."""

    template_name = "coaches/add_athlete.html"

    def post(self, request, *args, **kwargs):
        """Changing the post request.

        Enable search by athlete email.
        """
        form = AddAthleteForm(request.POST)
        coach = Coach.objects.get(profile__user=request.user)
        context = {
            "form": form,
            "coach": coach,
            "athlete_count": Athlete.objects.all().count(),
        }
        if form.is_valid():
            email = form.cleaned_data.get("email")
            context["new_athlete"] = Athlete.objects.get(
                profile__user__emailaddress__email=email
            )
        return render(
            request,
            self.template_name,
            context,
        )

    def get_context_data(self, *args, **kwargs):
        """Adding context data."""
        context = super().get_context_data(*args, **kwargs)
        context["form"] = AddAthleteForm
        context["coach"] = Coach.objects.get(profile=self.request.user.profile)
        return context

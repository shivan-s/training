"""Programme Session business logic."""

from collections import defaultdict
from typing import Any, Literal, Union

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, QuerySet
from django.db.models.functions import (
    ExtractDay,
    ExtractMonth,
    ExtractWeek,
    ExtractYear,
)
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.utils import timezone
from django.views.generic import TemplateView

from project.models import Athlete, Comment, ProgrammeSession


class BaseProgrammeView(LoginRequiredMixin, TemplateView):
    """Base Class-based view for Programme."""

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        """Adding context data."""
        context = super().get_context_data(*args, **kwargs)
        context["athlete"] = Athlete.objects.get(user=self.request.user)
        return context


class DateRangeCoachForm(forms.Form):
    """Form for dealing with post request for the ProgrammeView.

    This for is selecting the athlete's coach.
    """

    start = forms.DateField()
    end = forms.DateField()


class ProgrammeSessionListView(BaseProgrammeView):
    """View for training of a logged in Athlete."""

    template_name = "programme_sessions/list.html"

    def post(self, request, *args, **kwargs):
        """Changing the post request.

        The coach is selected to determine, which programme to display.
        """
        form = ProgrammeByCoachForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data["start"]
            end = form.cleaned_data["end"]
            athlete = self.request.user.athlete
            programmes = (
                ProgrammeSession.objects.filter(athlete=athlete)
                .filter(date__range=[start, end])
                .group_by()
            )
            return render(
                request,
                self.template_name,
                {"form": form, "programmes": programmes},
            )

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        """Adding context data."""
        context = super().get_context_data(*args, **kwargs)
        athlete = context["athlete"]
        coaches = athlete.coaches.all()
        programmes = ProgrammeSession.objects.filter(
            athlete=athlete
        ).group_by()
        context["coaches"] = coaches
        context["programmes"] = programmes
        return context


class CommentForm(forms.Form):
    """Comment."""

    comment = forms.CharField()


class ProgrammeSessionDetailView(BaseProgrammeView):
    """View for the detail view of the programme."""

    template_name = "programme_sessions/detail/detail.html"

    def get(self, request, *args, **kwargs):
        """\
        If athlete is not the coach, athlete can send programme link to coach.
        """
        programme_session = get_object_or_404(
            ProgrammeSession, reference_id=self.kwargs.get("pk")
        )
        if (
            self.request.user == programme_session.coach.user
            and programme_session.athlete.user != programme_session.coach.user
        ):
            return redirect(reverse("coach-programme-session-update"))
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        """Post."""
        form = CommentForm(request.POST)
        if form.is_valid():
            athlete = Athlete.objects.get(user=request.user)
            programme = get_object_or_404(
                ProgrammeSession, reference_id=self.kwargs.get("pk")
            )
            new_comment = Comment.objects.create(
                content=form.cleaned_data["comment"],
                author_content_object=athlete,
                location_content_object=programme,
            )
            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "new_comment": new_comment,
                    "programme": programme,
                },
            )
        else:
            raise Exception

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        """Context."""
        context = super().get_context_data(*args, **kwargs)
        athlete = context["athlete"]
        context["programme"] = get_object_or_404(
            ProgrammeSession, reference_id=self.kwargs.get("pk")
        )
        context["next_programme"] = None
        context["previous_programme"] = None

        programme_sessions = ProgrammeSession.objects.filter(athlete=athlete)
        for i, ps in enumerate(programme_sessions):
            if ps.reference_id == self.kwargs.get("pk"):
                if i > 0:
                    context["next_programme"] = programme_sessions[i - 1]
                if i < len(programme_sessions) - 1:
                    context["previous_programme"] = programme_sessions[i + 1]

        return context

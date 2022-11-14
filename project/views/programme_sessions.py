"""Programme Session business logic."""

from collections import defaultdict
from typing import Any, Literal, Union

from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, QuerySet
from django.db.models.functions import (
    ExtractDay,
    ExtractMonth,
    ExtractWeek,
    ExtractYear,
)
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from project.models import Athlete, ProgrammeSession


def get_programme_current_week(
    athlete: type[Athlete],
):
    """Obtain the current week for the programme."""
    programmes = (
        ProgrammeSession.objects.filter(athlete=athlete)
        .annotate(week=ExtractWeek(F("date")))
        .filter(week=timezone.now().isocalendar().week)
        .order_by("-date")
    )
    return programmes


GroupByProgrammeSession = dict[int, list[ProgrammeSession]]


def get_programme(
    athlete: type[Athlete],
    level: Literal["year", "month", "week", "day"] = "week",
    current: bool = True,
    previous: bool = False,
    next: bool = False,
) -> Union[QuerySet, list[ProgrammeSession]] | GroupByProgrammeSession | dict[
    int, GroupByProgrammeSession
] | dict[int, dict[int, GroupByProgrammeSession]] | dict[
    int, dict[int, dict[int, GroupByProgrammeSession]]
]:
    """Obtain the programme for a given athlete as a nested groupby.

    `level` defaults to "week", but can be changed to define level of nesting \
            required for the groupby.
    Args:
        user (T[Athlete]): Athlete instance model as part of the request.
        level (Literal["year", "month", "week", "day"]): nesting for groupby.
        current (bool): provide the current `level` set (e.g. current week).
        previous (bool): provide the previous `level` week (e.g previous week).
        next (bool): provide the programme for the next `level` (e.g. next \
                week).

    Returns:
        Programme sessions.
    """
    programmes = (
        ProgrammeSession.objects.filter(athlete=athlete)
        .order_by("-date")
        .annotate(year=ExtractYear(F("date")))
        .annotate(month=ExtractMonth(F("date")))
        .annotate(week=ExtractWeek(F("date")))
        .annotate(day=ExtractDay(F("date")))
    )

    return programmes

    def _generate_nested_defaultdict(depth: int):
        return (
            defaultdict(lambda: _generate_nested_defaultdict(depth - 1))
            if depth
            else dict
        )

    if level == "year":
        programmes_group_by = _generate_nested_defaultdict(2)
        for p in programmes:
            programmes_group_by[p.year][p.pk] = p
        return programmes_group_by
    elif level == "month":
        programmes_group_by = _generate_nested_defaultdict(3)
        for p in programmes:
            programmes_group_by[p.year][p.month][p.pk] = p
        return programmes_group_by
    elif level == "week":
        programmes_group_by = _generate_nested_defaultdict(4)
        for p in programmes:
            programmes_group_by[p.year][p.month][p.week][p.pk] = p
        return programmes_group_by
    elif level == "day":
        programmes_group_by = _generate_nested_defaultdict(5)
        for p in programmes:
            programmes_group_by[p.year][p.month][p.week][p.day][p.pk] = p
        return programmes_group_by
    else:
        return programmes


class BaseProgrammeView(LoginRequiredMixin, TemplateView):
    """Base Class-based view for Programme."""

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        """Adding context data."""
        context = super().get_context_data(*args, **kwargs)
        context["athlete"] = Athlete.objects.get(
            profile__user=self.request.user
        )
        return context


class ProgrammeByCoachForm(forms.Form):
    """Form for dealing with post request for the ProgrammeView.

    This for is selecting the athlete's coach.
    """

    coach = forms.CharField()


class ProgrammeSessionListView(BaseProgrammeView):
    """View for training of a logged in Athlete."""

    template_name = "programme/list.html"

    def post(self, request, *args, **kwargs):
        """Changing the post request.

        The coach is selected to determine, which programme to display.
        """
        form = ProgrammeByCoachForm(request.POST)
        if form.is_valid():
            coach_pk = form.cleaned_data["coach"]
            athlete = Athlete.objects.get(profile__user=request.user)
            programmes = get_programme(athlete, level=None).filter(
                coach__profile__user__pk=coach_pk
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
        programmes = get_programme(athlete=athlete)
        context["coaches"] = coaches
        # TODO: set ability to get a default coach view
        # If the selection is changed, this needs to reflect the displayed prgoramme
        # might have to set a param on the url?
        if coaches.last():
            default_coach = coaches.last()
            context["default_coach"] = default_coach
            context["programmes"] = programmes.filter(coach=default_coach)
        return context


# class ProgrammeSessionDetailForm(forms.ModelForm):
#     """Form allows athlete feedback."""
#
#     class Meta:
#         """Meta."""
#
#         model = ProgrammeSession


class ProgrammeSessionDetailView(BaseProgrammeView):
    """View for the detail view of the programme."""

    template_name = "programme/detail.html"

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        """Context."""
        context = super().get_context_data(*args, **kwargs)
        athlete = context["athlete"]
        qs = ProgrammeSession.objects.filter(athlete=athlete).filter(
            reference_id=self.kwargs.get("pk")
        )
        context["programme"] = get_object_or_404(qs)
        return context

"""IndexView."""

from collections import defaultdict
from itertools import groupby
from typing import Any, Literal
from typing import Type as T

from django.db.models import F
from django.db.models.functions import (
    ExtractDay,
    ExtractMonth,
    ExtractWeek,
    ExtractYear,
)
from django.utils import timezone
from django.views.generic import TemplateView

from project.models import Athlete, Profile, ProgrammeSession

GroupByProgrammeSession = dict[int, list[ProgrammeSession]]


def get_programme_current_week(
    athlete: T[Athlete],
):
    """Obtain the current week for the programme."""
    programmes = (
        ProgrammeSession.objects.filter(athlete=athlete)
        .annotate(week=ExtractWeek(F("date")))
        .filter(week=timezone.now().isocalendar().week)
        .order_by("-date")
    )
    return programmes


def get_programme(
    athlete: T[Athlete],
    level: Literal["year", "month", "week", "day"] = "week",
    current: bool = True,
    previous: bool = False,
    next: bool = False,
) -> list[ProgrammeSession] | GroupByProgrammeSession | dict[
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
        return list(programmes)


class IndexView(TemplateView):
    """Index view."""

    template_name = "index.html"

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        """Adding context data."""
        context = super().get_context_data(*args, **kwargs)
        # subtract 1 to exclude the admin view.
        context["count_profiles"] = Profile.objects.all().count() - 1
        if self.request.user.is_authenticated:
            # context["programmes"] = get_programme(
            #     Athlete.objects.get(profile__user=self.request.user),
            #     level="week",
            # )
            from datetime import timedelta

            days = timedelta(days=timezone.now().weekday())
            context["this_week"] = timezone.now() - days
            context["programmes"] = get_programme_current_week(
                Athlete.objects.get(profile__user=self.request.user)
            )
        return context

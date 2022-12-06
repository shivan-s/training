"""Manager for ProgrammeSession."""

from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime
from typing import TYPE_CHECKING, Union

from django.db import models
from django.db.models import F, Max, QuerySet
from django.db.models.functions import (
    ExtractDay,
    ExtractMonth,
    ExtractWeek,
    ExtractYear,
)
from django.utils import timezone

if TYPE_CHECKING:
    from ..athletes import Athlete
    from ..programme_sessions import ProgrammeSession

    GroupByProgrammeSession = dict[Union[QuerySet, list[ProgrammeSession]]]


class ProgrammeSessionQuerySet(models.QuerySet):
    """PrgrammeSession QuerySet."""

    def current_week(self):
        """Get current week of programmes."""
        return (
            self.annotate(week=ExtractWeek(F("date")))
            .annotate(year=ExtractYear(F("date")))
            .filter(year=timezone.now().isocalendar().year)
            .filter(week=timezone.now().isocalendar().week)
            .order_by("-date")
        )

    def next_week(self):
        """Get next week of programmes."""
        return (
            self.annotate(week=ExtractWeek(F("date")))
            .annotate(year=ExtractYear(F("date")))
            .filter(year=timezone.now().isocalendar().year)
            .filter(week=timezone.now().isocalendar().week + 1)
            .order_by("-date")
        )

    def previous_week(self):
        """Get next week of programmes."""
        return (
            self.annotate(week=ExtractWeek(F("date")))
            .annotate(year=ExtractYear(F("date")))
            .filter(year=timezone.now().isocalendar().year)
            .filter(week=timezone.now().isocalendar().week - 1)
            .order_by("-date")
        )

    def most_recent_week(self):
        """Get the most resent week of programmes."""
        # get the most recent programme session
        # determine the week
        # filter based on his week.
        recent = (
            self.order_by("date")
            .annotate(year=ExtractYear(F("date")))
            .annotate(week=ExtractWeek(F("date")))
        ).last()
        recent_week, recent_year = recent.week, recent.year
        return (
            self.annotate(week=ExtractWeek(F("date")))
            .annotate(year=ExtractYear(F("date")))
            .filter(year=recent_year)
            .filter(week=recent_week)
        )

    def group_by(
        self,
    ) -> Union[
        QuerySet, list[ProgrammeSession]
    ] | GroupByProgrammeSession | dict[int, GroupByProgrammeSession] | dict[
        int, dict[int, GroupByProgrammeSession]
    ] | dict[
        int, dict[int, dict[int, GroupByProgrammeSession]]
    ]:
        """Obtain the programme for a given athlete as a nested groupby.

        Returns:
            Programme sessions.
        """
        programmes = (
            self.annotate(year=ExtractYear(F("date")))
            .annotate(month=ExtractMonth(F("date")))
            .annotate(week=ExtractWeek(F("date")))
            .annotate(day=ExtractDay(F("date")))
            .order_by("-year", "-week", "month", "day", "session_type")
        )

        tree = lambda: defaultdict(tree)
        programmes_group_by = tree()

        def _get_month(d: datetime) -> int:
            year = d.isocalendar().year
            week = d.isocalendar().week
            return date.fromisocalendar(year=year, week=week, day=1).month

        for p in programmes:
            programmes_group_by[p.date.isocalendar().year][_get_month(p.date)][
                p.date.isocalendar().week
            ][p.date][p.pk] = p

        for year in programmes_group_by.values():
            year.default_factory = None
            for month in year.values():
                month.default_factory = None
                for week in month.values():
                    week.default_factory = None
                    for day in week.values():
                        day.default_factory = None

        return dict(programmes_group_by)


class ProgrammeSessionManager(models.Manager):
    """ProgrammeSession Manager."""

    def get_queryset(self):
        """Redefine queryset."""
        return ProgrammeSessionQuerySet(self.model, using=self._db)

    def current_week(
        self,
        *arg,
        **kwargs,
    ):
        """Obtain the current week for the programme."""
        return self.get_queryset().current_week()

    def next_week(
        self,
        *args,
        **kwargs,
    ):
        """Obtain the next week for the programme."""
        return self.get_queryset().next_week()

    def previous_week(
        self,
        *args,
        **kwargs,
    ):
        """Obtain the previous week for the programme."""
        return self.get_queryset().previous_week()

    def group_by(self, *args, **kwargs):
        """Group by return."""
        return self.get_queryset().group_by(*args, **kwargs)

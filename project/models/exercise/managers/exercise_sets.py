"""Manager for ExerciseSet."""

from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime
from typing import TYPE_CHECKING, Union

from django.db import models
from django.db.models import F, Max, QuerySet
from django.db.models.functions import ExtractWeek, ExtractYear
from django.utils import timezone

if TYPE_CHECKING:
    from ... import Athlete
    from .. import ExerciseSet

    # GroupByProgrammeSession = dict[Union[QuerySet, list[ProgrammeSession]]]


class ExerciseSetQuerySet(models.QuerySet):
    """QuerySet."""

    def current_week(self):
        """Get current week of exercise sets."""
        return (
            self.select_related("intended")
            .prefetch_related("intended__programme_session")
            .annotate(
                year=F("intended__programme_session__date__year"),
                week=F("intended__programme_session__date__week"),
            )
            .filter(
                week=timezone.now().isocalendar().week,
                year=timezone.now().isocalendar().year,
            )
            .order_by("-intended__programme_session__date")
        )


class ExerciseSetManager(models.Manager):
    """Manager"""

    def get_queryset(self):
        """Redefine."""
        return ExerciseSetQuerySet(self.model, using=self._db)

    def current_week(self, *args, **kwargs):
        """Obtain current week of exercise sets for programming."""
        return self.get_queryset().current_week()

"""Utility functions for models."""

from __future__ import annotations

from typing import TYPE_CHECKING, Union

from django.db.models import Max

from .. import ProgrammeSession
from . import Exercise, ExerciseSet


def get_max_exercise_order(programme_session: type[ProgrammeSession]) -> int:
    """Return the max order number."""
    existing = Exercise.objects.filter(programme_session=programme_session)
    if not existing.exists():
        return 1
    else:
        return existing.aggregate(max_order=Max("order"))["max_order"] + 1


def reorder_exercise(
    programme_session: type[ProgrammeSession],
) -> None:
    """Reorder."""
    existing = Exercise.objects.filter(programme_session=programme_session)
    if not existing.exists():
        return []
    count = existing.count()
    new_order = range(1, count + 1)

    for order, exercise in zip(new_order, existing):
        exercise.order = order


def get_max_exercise_set_order(
    exercise: type[Exercise],
) -> int:
    """Return the max order number."""
    existing = ExerciseSet.objects.filter(intended=exercise)
    if existing.exists():
        return 1
    else:
        return existing.aggregate(max_order=Max("order"))["max_order"] + 1


def reorder_exercise_set(
    exercise: type[ExerciseSet],
) -> None:
    """Reorder."""
    existing = Exercise.objects.filter(programme_session=programme_session)
    if not existing.exists():
        return []
    count = existing.count()
    new_order = range(1, count + 1)

    for order, exercise in zip(new_order, existing):
        exercise.order = order

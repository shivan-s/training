"""ProgrammeSession admin."""

from typing import Type

import nested_admin
from django.contrib import admin

from project.models import (
    Exercise,
    ExerciseSet,
    ExerciseType,
    ProgrammeSession,
)


class IntendedExerciseSetInline(nested_admin.NestedTabularInline):
    model: Type[ExerciseSet] = ExerciseSet
    fk_name: str = "intended"
    extra: int = 1


class OutcomeExerciseSetInline(nested_admin.NestedTabularInline):
    model: Type[ExerciseSet] = ExerciseSet
    fk_name: str = "outcome"
    extra: int = 0


class ExerciseInline(nested_admin.NestedStackedInline):
    model: Type[Exercise] = Exercise
    inlines = [IntendedExerciseSetInline, OutcomeExerciseSetInline]
    extra = 1


class ExerciseTypeInline(nested_admin.NestedStackedInline):
    model = ExerciseType


@admin.register(ProgrammeSession)
class ProgrammeSessionAdmin(nested_admin.NestedModelAdmin):
    """ProgrammeSession admin view."""

    model = ProgrammeSession
    readonly_fields = ("reference_id",)
    raw_id_fields = ("coach", "athlete")
    inlines = [ExerciseInline]
    fields = (
        "coach",
        "athlete",
        "date",
        "session_type",
        "start",
        "end",
        "coach_notes",
    )

"""ProgrammeSession admin."""

from collections.abc import Iterable

import nested_admin
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from simple_history.admin import SimpleHistoryAdmin

from project.models import Exercise, ProgrammeSession

from .base import BaseCommentInline, BaseExerciseSetInline, InlineType


class CommentInline(BaseCommentInline):
    """Comment Inline."""

    ct_field = "location_ct"
    ct_fk_field = "location_object_id"
    readonly_fields: Iterable[str] = ("author_content_object", "content")
    fields: Iterable[str] = ("author_content_object", "content")


class IntendedExerciseSetInline(BaseExerciseSetInline):
    """Intended Inline."""

    verbose_name = _("intended")
    fk_name = "intended"
    extra = 1


class OutcomeExerciseSetInline(BaseExerciseSetInline):
    """Outcome Inline."""

    verbose_name = _("outcome")
    fk_name = "outcome"


class ExerciseInline(nested_admin.NestedStackedInline):
    """ExerciseInline."""

    model: type[Exercise] = Exercise
    inlines: InlineType = (
        IntendedExerciseSetInline,
        OutcomeExerciseSetInline,
        CommentInline,
    )
    extra = 1


@admin.register(ProgrammeSession)
class ProgrammeSessionAdmin(nested_admin.NestedModelAdmin, SimpleHistoryAdmin):
    """ProgrammeSession admin view."""

    model: type[ProgrammeSession] = ProgrammeSession
    readonly_fields: Iterable[str] = ("reference_id", "deleted", "deleted_at")
    raw_id_fields: Iterable[str] = ("coach", "athlete")
    inlines: InlineType = (
        ExerciseInline,
        CommentInline,
    )
    history_list_display: Iterable[str] = []
    fields: Iterable[str] = (
        "reference_id",
        "deleted",
        "deleted_at",
        "date",
        "session_type",
        "published",
        "start",
        "end",
        "coach_notes",
    )

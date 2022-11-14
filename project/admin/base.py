"""Base Inline and Admin classes."""

from typing import Type
from collections.abc import Iterable

import nested_admin

from project.models import Comment, ExerciseSet

InlineType = Iterable[
    type[nested_admin.NestedStackedInline]
    | type[nested_admin.NestedTabularInline]
    | type[nested_admin.NestedGenericStackedInline]
    | type[nested_admin.NestedGenericTabularInline]
]


class BaseExerciseSetInline(nested_admin.NestedTabularInline):
    """ExerciseSet Inline."""

    model: type[ExerciseSet] = ExerciseSet
    fields: Iterable[str] = ("sets", "repetitions", "weight", "weight_unit")
    extra = 0


class BaseCommentInline(nested_admin.NestedGenericTabularInline):
    """Comment Inline."""

    model: type[Comment] = Comment
    fields: Iterable[str] = ("content",)
    extra = 0

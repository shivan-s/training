"""Base Inline and Admin classes."""

from typing import Iterable, Type

import nested_admin

from project.models import Comment, ExerciseSet

InlineType = Iterable[
    Type[nested_admin.NestedStackedInline]
    | Type[nested_admin.NestedTabularInline]
    | Type[nested_admin.NestedGenericStackedInline]
    | Type[nested_admin.NestedGenericTabularInline]
]


class BaseExerciseSetInline(nested_admin.NestedTabularInline):
    """ExerciseSet Inline."""

    model: Type[ExerciseSet] = ExerciseSet
    fields: Iterable[str] = ("sets", "repetitions", "weight", "weight_unit")
    extra = 0


class BaseCommentInline(nested_admin.NestedGenericTabularInline):
    """Comment Inline."""

    model: Type[Comment] = Comment
    fields: Iterable[str] = ("content",)
    extra = 0

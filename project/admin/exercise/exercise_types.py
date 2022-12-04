"""Exercise Type."""

import nested_admin
from django.contrib import admin

from project.models import ExerciseType


class ExerciseCategoryInline(nested_admin.NestedStackedInline):
    """Creating exercise categories."""

    model = ExerciseType.categories.through
    extra = 0


@admin.register(ExerciseType)
class ExerciseTypeAdmin(nested_admin.NestedModelAdmin):
    """ExerciseType admin view."""

    model = ExerciseType
    readonly_fields = ("reference_id",)
    inlines = [ExerciseCategoryInline]
    raw_id_fields = ("creator",)
    related_lookup_fields = {
        "creator": ["creator"],
    }
    fields = (
        "creator",
        "name",
        "description",
        "is_private",
        "categories",
        "starred",
    )

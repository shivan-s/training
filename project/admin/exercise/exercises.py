"""Exercise admin."""

from django.contrib import admin

from project.models import Exercise


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    """Exercise admin view."""

    model = Exercise
    readonly_fields = ("reference_id", "tonnage")

    fields = (
        "coach_notes",
        "weight_unit",
        "comments",
    )

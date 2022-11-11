"""ExerciseSet admin."""

from django.contrib import admin

from project.models import ExerciseSet


@admin.register(ExerciseSet)
class ExerciseSetAdmin(admin.ModelAdmin):
    """ExerciseSet admin view."""

    model = ExerciseSet
    readonly_fields = ("reference_id",)
    fields = ("repetitions", "weight")

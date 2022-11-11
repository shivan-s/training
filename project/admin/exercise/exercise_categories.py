"""ExerciseCategory admin."""

from django.contrib import admin

from project.models import ExerciseCategory


@admin.register(ExerciseCategory)
class ExerciseCategoryAdmin(admin.ModelAdmin):
    """ExerciseCategory admin view."""

    model = ExerciseCategory
    readonly_fields = ("reference_id",)
    fields = ("name", "parent")

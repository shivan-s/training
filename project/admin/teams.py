"""TeamAdmin."""

from django.contrib import admin

from project.models import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """ProgrammeSession admin view."""

    model = Team
    readonly_fields = ("reference_id",)
    raw_id_fields = ("creator",)
    fields = (
        "name",
        "description",
        "creator",
        "coaches",
        "athletes",
    )

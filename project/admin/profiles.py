"""ProfileAdmin."""

import nested_admin
from django.contrib import admin

from project.models import Athlete, Coach, Profile


class CoachInline(nested_admin.NestedStackedInline):
    """Inline for Coach in Profile."""

    model = Coach


class AthleteInline(nested_admin.NestedStackedInline):
    """Inline for Athlete in the Profile."""

    model = Athlete


@admin.register(Profile)
class ProfileAdmin(nested_admin.NestedModelAdmin):
    """Profile admin view."""

    model = Profile
    search_fields = ("user__name", "user__email")
    raw_id_fields = ("user",)
    list_display = ("user",)
    fields = ("name", "avatar")
    inlines = (CoachInline, AthleteInline)

"""CoachAdmin."""

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from project.models import Coach


@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    """Coach admin view."""

    model = Coach
    search_fields = ("profile__name", "profile__user__email")
    raw_id_fields = ("profile", "athlete")
    list_display = ("profile", "view_coaches_link")

    def view_coaches_link(self, obj):
        """Provide link to athletes for this coach."""
        count = obj.athletes.count()
        url = (
            reverse("admin:project_coach_changelist")
            + "?"
            + urlencode({"athletes": f"{obj.athletes}"})
        )
        return format_html('<a href="{}" Coaches</a>', url, count)

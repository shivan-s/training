"""CoachAdmin."""

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from project.models import Athlete


@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    """Athlete admin view."""

    model = Athlete
    search_fields = ("profile__name", "profile__user__email")
    raw_id_fields = ("profile", "coach")
    list_display = ("profile", "view_coaches_link")

    def view_coaches_link(self, obj):
        count = obj.coaches.count()
        """Provide link to coaches for this athlete."""
        print(obj.coaches.count())
        print(obj)
        url = (
            reverse("admin:project_coach_changelist")
            + "?"
            + urlencode({"coaches": f"{obj.coaches}"})
        )
        return format_html('<a href="{}" {} Coaches</a>', url, count)

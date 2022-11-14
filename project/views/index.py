"""IndexView."""

from datetime import timedelta
from typing import Any

from django.utils import timezone
from django.views.generic import TemplateView

from project.models import Athlete, Profile

from .programme_sessions import get_programme_current_week


class IndexView(TemplateView):
    """Index view."""

    template_name = "index.html"

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        """Adding context data."""
        context = super().get_context_data(*args, **kwargs)
        # subtract 1 to exclude the admin view.
        context["count_profiles"] = Profile.objects.all().count() - 1
        if self.request.user.is_authenticated:
            # days - days from the first day of the week.
            days = timedelta(days=timezone.now().weekday())
            context["this_week"] = timezone.now() - days
            context["programmes"] = get_programme_current_week(
                Athlete.objects.get(profile__user=self.request.user)
            )
        return context

"""IndexView."""

from datetime import timedelta
from typing import Any

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils import timezone
from django.views.generic import TemplateView

from project.models import ExerciseSet, ProgrammeSession
from project.tasks import count_users

User = get_user_model()


class IndexView(TemplateView):
    """Index view."""

    template_name = "index/index.html"

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        """Adding context data."""
        context = super().get_context_data(*args, **kwargs)
        total_users = cache.get("total_users")
        count_users.delay()
        if total_users:
            context["total_users"] = total_users
        else:
            context["total_users"] = User.objects.all().count()
        # TODO: determine if the default home page is athlete view or coach view.
        if self.request.user.is_authenticated:
            # days - days from the first day of the week.
            days_from_start = timedelta(days=timezone.now().weekday())
            start_week = timezone.now() - days_from_start
            context["start_week"] = start_week
            context["end_week"] = start_week + timedelta(days=7)
            athlete = self.request.user.athlete
            exercise_sets = ExerciseSet.objects.filter(
                intended__programme_session__athlete=athlete
            ).current_week()
            # context["exercise_sets"] = exercise_sets
            context["programmes"] = (
                ProgrammeSession.objects.filter(athlete=athlete)
                .current_week()
                .group_by()
            )
        return context

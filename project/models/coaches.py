"""Coach model."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from .base import BaseAthleteCoachModel


class Coach(BaseAthleteCoachModel):
    """Coach model.

    Coaches create the programmes for their athletes.

    They also have the ability to create exercises, and teams.
    """

    athletes = models.ManyToManyField(
        "project.Athlete",
        verbose_name=_("athletes"),
        blank=True,
    )

    def __str__(self):
        """Represent string."""
        if self.profile.name:
            return f"C: {self.profile.user.email} ({self.profile.name})"
        return f"C: {self.profile.user.email}"

    class Meta(BaseAthleteCoachModel.Meta):
        """Setting for model.

        Providing a plural name for coach (coaches).
        """

        verbose_name_plural = "coaches"

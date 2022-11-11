"""Athlete model."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from .base import BaseAthleteCoachModel


class Athlete(BaseAthleteCoachModel):
    """Athlete model.

    Athletes are the ones who train, obviously. They receive a programme from \
            the coach.

    They also provide feedback on the programme and exercises.
    """

    coaches = models.ManyToManyField(
        "project.Coach", verbose_name=_("coaches"), blank=True
    )

    def __str__(self):
        """Represent string."""
        if self.profile.name:
            return f"A: {self.profile.user.email} ({self.profile.name})"
        return f"A: {self.profile.user.email}"

    class Meta(BaseAthleteCoachModel.Meta):
        """Settings for Model.

        "Inheriting the `app_label`."
        """

        ...

"""Athlete model."""

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .base import BaseAthleteCoachModel
from .managers import AthleteManager

MAX_COACHES = 5


class Athlete(BaseAthleteCoachModel):
    """Athlete model.

    Athletes are the ones who train, obviously. They receive a programme from \
            the coach.

    They also provide feedback on the programme and exercises.
    """

    coaches = models.ManyToManyField(
        "project.Coach", verbose_name=_("coaches"), blank=True
    )
    comments = GenericRelation(
        "project.Comment",
        related_query_name="athlete",
        content_type_field="author_ct",
        object_id_field="author_object_id",
    )
    # TODO: set up a "default coach"

    objects = AthleteManager()

    def get_absolute_url(self):
        """Provide the url for the instance."""
        return reverse("project:athlete-detail", kwargs={"pk": self.pk})

    def get_coach_programme_sessions_url(self) -> str:
        """Provide absolute url for the athlete's programme sessions.

        This is used for a coach viewing and athlete's programme as a coach.
        """
        kwargs = {"pk": self.pk}
        return reverse("project:coach-programme-session-list", kwargs=kwargs)

    def get_hx_coach_programme_session_new_url(self) -> str:
        """Provides url for creating a new programme session.

        This will work for an athlete instance and this is mainly for coach \
                view."""
        kwargs = {"athlete_pk": self.pk}
        return reverse("project:hx-coach-programme-session-new", kwargs=kwargs)

    def get_hx_coach_programme_session_week_duplicate_url(self):
        """Provide url for duplicating a programme session.

        This will work for an athlete instance and this is mainly for coach \
                view.
        """
        kwargs = {"pk": self.pk}
        return reverse(
            "project:hx-coach-programme-session-week-duplicate", kwargs=kwargs
        )

    def clean(self, *args, **kwargs):
        """Customise validation.

        1. Athlete can only have max number of coaches.
        """
        errors = []
        # Athlete max number of coaches
        if self.coaches.count() > MAX_COACHES:
            raise ValidationError(
                {"coaches": "Maximum number exceeded. Max: %(max_coaches)s."},
                code="max-coaches",
                params={"max_coaches": MAX_COACHES},
            )

        if len(errors) > 0:
            error_msg = "\n".join(errors)
            raise ValidationError(
                "%(error_msg)s",
                code="Invalid Attempt",
                params={
                    "error_msg": error_msg,
                },
            )
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Enforce custom validation."""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        """Represent string."""
        return f"A: {self.user.name}"

    class Meta(BaseAthleteCoachModel.Meta):
        """Settings for Model.

        "Inheriting the `app_label`."
        """

        ...

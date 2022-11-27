"""Athlete model."""

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
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
        if self.profile.name:
            return f"A: {self.profile.user.email} ({self.profile.name})"
        return f"A: {self.profile.user.email}"

    class Meta(BaseAthleteCoachModel.Meta):
        """Settings for Model.

        "Inheriting the `app_label`."
        """

        ...

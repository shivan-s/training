"""Exercise model."""

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _
from hashid_field import HashidAutoField

from config.settings import HASHID_FIELD_SALT
from project.models.base import BaseModel


class Exercise(BaseModel):
    """Exercise model."""

    reference_id = HashidAutoField(
        primary_key=True, salt=f"set_{HASHID_FIELD_SALT}"
    )
    programme_session = models.ForeignKey(
        "project.ProgrammeSession",
        on_delete=models.CASCADE,
        verbose_name=_("Programming sessions"),
        blank=True,
        null=True,
    )
    exercise_type = models.ForeignKey(
        "project.ExerciseType",
        on_delete=models.CASCADE,
        verbose_name=_("exercise"),
    )

    coach_notes = models.TextField(
        _("coach's notes"),
        blank=True,
        null=True,
    )
    comments = GenericRelation(
        "project.Comment",
        related_query_name="exercise",
        content_type_field="location_ct",
        object_id_field="location_object_id",
    )
    order = models.PositiveSmallIntegerField()

    def get_hx_edit_url(self) -> str:
        kwargs = {
            "athlete_pk": self.programme_session.athlete.pk,
            "programme_session_pk": self.programme_session.pk,
            "pk": self.pk,
        }
        return reverse(
            "project:hx-coach-exercise-update",
            kwargs=kwargs,
        )

    def __str__(self) -> str:
        """Represent string."""
        return f"{self.exercise_type}"

    class Meta(BaseModel.Meta):
        """Settings for model."""

        ...

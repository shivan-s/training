"""Exercise model."""

from django.db import models
from django.utils.translation import gettext_lazy as _
from hashid_field import HashidAutoField

from config.settings import HASHID_FIELD_SALT
from project.models.base import BaseModel


class Exercise(BaseModel):
    """Exercise model."""

    class WeightUnit(models.TextChoices):
        """Choices for `weight_unit`."""

        KILOGRAMS = "KG", _("kilograms")
        POUNDS = "LB", _("pounds")

    reference_id = HashidAutoField(
        primary_key=True, salt=f"set_{HASHID_FIELD_SALT}"
    )
    programme_session = models.ForeignKey(
        "project.ProgrammeSession",
        on_delete=models.CASCADE,
        verbose_name=_("Programming sessions"),
    )
    exercise_type = models.ForeignKey(
        "project.ExerciseType",
        on_delete=models.CASCADE,
        verbose_name=_("exercise_type"),
    )

    weight_unit = models.CharField(
        max_length=2,
        choices=WeightUnit.choices,
        default=WeightUnit.KILOGRAMS,
    )

    coach_notes = models.TextField(
        _("coach's notes"),
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        """Represent string."""
        return f"{self.exercise_type}"

    class Meta(BaseModel.Meta):
        """Settings for model."""

        ...

"""ExerciseSet model."""

import inflect
from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _
from hashid_field import HashidAutoField

from config.settings import HASHID_FIELD_SALT
from project.models.base import BaseModel

inf = inflect.engine()


class ExerciseSet(BaseModel):
    """This model is used for the Exercise model.

    e.g. A set is 10 reps of weight 10

    The `weight_unit` is defined on the Exercise model.

    The `intended` and `outcome` field relate to an exercise for which the \
            former relates to what the coach has intended in the programme. \
            The later relates to what the athlete has performed for that \
            exercise.
    """

    class WeightUnit(models.TextChoices):
        """Choices for `weight_unit`."""

        KILOGRAMS = "KG", _("kilograms (kg)")
        POUNDS = "LB", _("pounds (lbs)")
        PERCENTAGE = "PE", _("percentage (%)")

    reference_id = HashidAutoField(
        primary_key=True, salt=f"set_{HASHID_FIELD_SALT}"
    )
    sets = models.PositiveIntegerField(_("sets"), blank=True, default=1)
    repetitions = models.PositiveIntegerField(_("repetitions"))
    weight = models.DecimalField(
        _("weight"),
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[validators.MinValueValidator(limit_value=0)],
    )
    weight_unit = models.CharField(
        max_length=2,
        choices=WeightUnit.choices,
        default=WeightUnit.KILOGRAMS,
        blank=True,
        null=True,
    )
    intended = models.ForeignKey(
        "project.Exercise",
        on_delete=models.CASCADE,
        verbose_name=_("intended exercise"),
        related_name="intended",
        blank=True,
        null=True,
    )
    outcome = models.ForeignKey(
        "project.Exercise",
        on_delete=models.CASCADE,
        verbose_name=_("outcome exercise"),
        related_name="outcome",
        blank=True,
        null=True,
    )

    @property
    def display_shortened_weight_unit(self, WeightUnit=WeightUnit) -> str:
        """Display shorten weight unit.

        e.g. kilograms = kg
        """
        return {
            WeightUnit.KILOGRAMS: "kg",
            WeightUnit.POUNDS: "lbs",
            WeightUnit.PERCENTAGE: "%",
        }.get(self.weight_unit)

    def __str__(self) -> str:
        """Represent string."""
        return " ".join(
            [
                str(self.weight).rstrip("0").rstrip("."),
                f"{self.display_shortened_weight_unit} x {self.repetitions}",
                f"{inf.plural('rep', self.repetitions)}",
                f"x {self.sets}",
                inf.plural("set", self.sets),
            ]
        )

        # + f"{x {self.sets} {inf.plural('set', self.sets)}'} if self.sets > 1  else ''}"

    class Meta(BaseModel.Meta):
        """Settings for model."""

        ...

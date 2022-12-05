"""ExerciseSet model."""

import inflect
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from hashid_field import HashidAutoField

from config.settings import HASHID_FIELD_SALT
from project.models.base import BaseModel

# dealing with plurals
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
        POUNDS = "LBS", _("pounds (lbs)")
        PERCENTAGE = "PER", _("percentage (%)")
        RPE = "RPE", (_("rate of perceived exertion (RPE)"))

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
        max_length=3,
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
            WeightUnit.RPE: "RPE",
        }.get(self.weight_unit)

    # TODO: make this work
    # def copy_sets(self) -> None:
    #     """Set the `outcome` and to the exercise (linked via `intended`).
    #
    #     This indicates that the athlete completed the sets successfully.
    #     """
    #     self.outcome = self.intended

    @property
    def display_weight(self) -> str:
        """Provide human readable way of determining sets."""
        return str(self.weight).rstrip("0").rstrip(".")

    @property
    def display_sets(self) -> str:
        """Provide human readable way of determining sets."""
        return f"{self.sets} {inf.plural('set', self.sets)}"

    @property
    def display_repetitions(self) -> str:
        """Provide human readable way of determining repetitions."""
        return f"{self.repetitions} {inf.plural('rep', self.repetitions)}"

    def get_hx_edit_url(self) -> str:
        kwargs = {
            "athlete_pk": self.intended.programme_session.athlete.pk,
            "programme_session_pk": self.intended.programme_session.pk,
            "exercise_pk": self.intended.pk,
            "pk": self.pk,
        }
        return reverse(
            "project:hx-coach-exercise-set-update",
            kwargs=kwargs,
        )

    def clean(self, WeightUnit=WeightUnit, *args, **kwargs):
        """Customise validation.

        1. Ensure RPE can only between 0 and 10.
        """
        errors = []
        if self.weight_unit == WeightUnit.RPE and self.weight > 12:
            raise ValidationError(
                {
                    "weight": "RPE selected. Weight can only be set between 0 to 12, not %(weight)s"
                },
                code="rpe-error",
                params={
                    "weight": self.weight,
                },
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

    def __str__(self) -> str:
        """Represent string."""
        return " ".join(
            [
                self.display_weight,
                self.display_shortened_weight_unit,
                "x",
                self.display_repetitions,
                "x",
                self.display_sets,
            ]
        )

    class Meta(BaseModel.Meta):
        """Settings for model."""

        ...

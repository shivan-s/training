"""ExerciseSet model."""

from django.db import models
from django.utils.translation import gettext_lazy as _
from hashid_field import HashidAutoField

from config.settings import HASHID_FIELD_SALT
from project.models.base import BaseModel


class ExerciseSet(BaseModel):
    """This model is used for the Exercise model.

    e.g. A set is 10 reps of weight 10

    The `weight_unit` is defined on the Exercise model.

    The `intended` and `outcome` field relate to an exercise for which the \
            former relates to what the coach has intended in the programme. \
            The later relates to what the athlete has performed for that \
            exercise.
    """

    reference_id = HashidAutoField(
        primary_key=True, salt=f"set_{HASHID_FIELD_SALT}"
    )
    sets = models.PositiveIntegerField(_("sets"), blank=True, default=1)
    repetitions = models.PositiveIntegerField(_("repetitions"))
    weight = models.DecimalField(
        _("weight"), max_digits=5, decimal_places=1, null=True, blank=True
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

    def __str__(self) -> str:
        """Represent string."""
        return f"{self.repetitions} x {self.weight}"

    class Meta(BaseModel.Meta):
        """Settings for model."""

        ...

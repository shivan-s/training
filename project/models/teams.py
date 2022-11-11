"""Team model."""

from django.db import models
from django.utils.translation import gettext_lazy as _
from hashid_field import HashidAutoField

from config.settings import HASHID_FIELD_SALT

from .base import BaseModel


class Team(BaseModel):
    """Represent a collection of athletes and coaches.

    An example would be a weightlifting club.
    """

    reference_id = HashidAutoField(
        primary_key=True, salt=f"team_{HASHID_FIELD_SALT}"
    )
    name = models.CharField(_("name"), max_length=155, unique=True)
    description = models.TextField(_("description"), max_length=1000)
    creator = models.ForeignKey(
        "project.Coach",
        on_delete=models.CASCADE,
        verbose_name=_("creator of team"),
        related_name="team_creator",
    )
    coaches = models.ManyToManyField(
        "project.Coach",
        verbose_name=_("list of coaches"),
        blank=True,
    )
    athletes = models.ManyToManyField(
        "project.Athlete",
        verbose_name=_("list of athletes"),
        blank=True,
    )

    def __str__(self):
        """Represent string."""
        return self.name

    class Meta(BaseModel.Meta):
        """Settings for model."""

        ...

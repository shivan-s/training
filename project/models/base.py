"""Contains Abstract models for children models to inherit from.

Some important features include soft deletion and historical field records.
"""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from softdelete.models import SoftDeleteObject


class BaseModel(SoftDeleteObject, models.Model):
    """Abstract model for all models to inherit from."""

    history = HistoricalRecords(inherit=True)

    class Meta:
        """Options.

        `abstract = True` to make this an inherited model.

        Also, set the `app_label` for children models.
        """

        abstract = True
        app_label = "project"


class BaseAthleteCoachModel(BaseModel):
    """Abstract model for Athlete and Coach to inherit from."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name=_("user"),
    )

    class Meta(BaseModel.Meta):
        """Options.

        `abstract` set to `True` to make this an inherited model.
        """

        abstract = True

    def __str__(self):
        """Represent string."""
        return f"{self.__class__.name} - {self.user.__str__()}"

    @property
    def name(self) -> str:
        return self.user.name

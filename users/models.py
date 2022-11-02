"""Model for CustomUser."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from hashid_field import HashidAutoField
from simple_history.models import HistoricalRecords
from softdelete.models import SoftDeleteObject

from config.settings import HASHID_FIELD_SALT


class CustomUser(AbstractUser, SoftDeleteObject):
    """CustomUser model."""

    reference_id = HashidAutoField(
        primary_key=True, salt=f"{HASHID_FIELD_SALT}"
    )
    name = models.CharField(_("name"), max_length=155, blank=True, null=True)
    email = models.EmailField(_("email address"), unique=True)
    history = HistoricalRecords()

    def __str__(self):
        """Setting."""
        return self.email

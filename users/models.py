"""Model for CustomUser."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from hashid_field import HashidAutoField
from simple_history.models import HistoricalRecords
from softdelete.models import SoftDeleteObject

from config.settings import HASHID_FIELD_SALT


class CustomUser(AbstractUser, SoftDeleteObject):
    """User model for application.

    Invokes soft deletetion.

    Links to a single Coach and Athlete model.
    """

    reference_id = HashidAutoField(
        primary_key=True, salt=f"custom_user_{HASHID_FIELD_SALT}"
    )
    email = models.EmailField(_("email address"), unique=True)
    history = HistoricalRecords()

    def __str__(self):
        """Represent string."""
        return self.email

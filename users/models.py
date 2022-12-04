"""Model for CustomUser."""

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField
from hashid_field import HashidAutoField
from simple_history.models import HistoricalRecords
from softdelete.models import SoftDeleteObject

from .managers import CustomUserManager

# TODO: create validation for name
# alphabet = RegexValidator(
#     r"^[a-zA-Z\s]*$", "Only alphabet characters are allowed."
# )
alphanumeric = RegexValidator(
    r"^\w*$", "Only alphabet, numbers, and underscores ('_') are accepted."
)


class CustomUser(AbstractBaseUser, PermissionsMixin, SoftDeleteObject):
    """User model for application.

    Invokes soft deletetion.

    Links to a single Coach and Athlete model.
    """

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    reference_id = HashidAutoField(
        primary_key=True, salt=f"custom_user_{settings.HASHID_FIELD_SALT}"
    )
    email = models.EmailField(_("e-mail"), unique=True)
    name = models.CharField(_("display name"), max_length=50)

    is_active = models.BooleanField(_("is active"), default=True)
    is_superuser = models.BooleanField(_("is superuser"), default=False)
    is_staff = models.BooleanField(_("is staff"), default=False)

    date_joined = models.DateTimeField(
        _("date joined"), default=timezone.now()
    )
    last_login = models.DateTimeField(_("last login"), blank=True, null=True)

    avatar = ThumbnailerImageField(
        upload_to=("images/"), null=True, blank=True
    )
    is_private = models.BooleanField(_("is_private"), default=False)

    history = HistoricalRecords()

    objects = CustomUserManager()

    def get_full_name(self):
        """Return the name of the user."""
        return self.name

    def get_short_name(self):
        """Shadows `self.get_full_name()`"""
        return self.get_full_name()

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Email the user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        """Represent string."""
        return f"{self.pk} - {self.email} {self.name}"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

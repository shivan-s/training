"""Profile model."""

# allauth.account.signals.email_confirmed(request, email_address)

from django.db import models
from django.utils.translation import gettext_lazy as _
from sorl.thumbnail import ImageField

from config.settings import AUTH_USER_MODEL

from .base import BaseModel


class Profile(BaseModel):
    """Profile model."""

    user = models.OneToOneField(
        AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True
    )
    name = models.CharField(_("name"), max_length=155, blank=True, null=True)
    avatar = ImageField(upload_to="images/", null=True, blank=True)
    follows = models.ManyToManyField(
        "self", related_name="followed_by", symmetrical=False, blank=True
    )
    is_private = models.BooleanField(_("is_private"), default=False)

    def __str__(self):
        """Represent string."""
        if self.name:
            return f"{self.name}"
        return f"{str(self.user.reference_id)}"

    class Meta(BaseModel.Meta):
        """Options."""

        ...

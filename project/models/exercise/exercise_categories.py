"""ExerciseType model."""

from django.db import models
from django.utils.translation import gettext_lazy as _
from hashid_field import HashidAutoField
from mptt.models import MPTTModel, TreeForeignKey
from simple_history.models import HistoricalRecords

from config.settings import HASHID_FIELD_SALT


class ExerciseCategory(MPTTModel):
    """Categorise exercises and can be created by the community.

    The `BaseModel` is not inherited because:

    This is implemented because of the HistoryRecord fields cannot be \
            declared at the base and then overwritten.

    `MPTTModel` comes with extra fields under the hood that do not get added \
            to the history table and must be excluded.
    """

    reference_id = HashidAutoField(
        primary_key=True, salt=f"category_{HASHID_FIELD_SALT}"
    )
    name = models.CharField(_("exercise name"), max_length=25, unique=True)
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    history = HistoricalRecords(
        excluded_fields=["lft", "rght", "tree_id", "level"]
    )

    def __str__(self) -> str:
        """Represent string."""
        return f"{self.name}"

    class Meta:
        """Settings for model."""

        app_label = "project"
        verbose_name_plural = "exercise categories"

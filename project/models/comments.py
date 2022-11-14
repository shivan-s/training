"""Comment model."""

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
from hashid_field import HashidAutoField

from config.settings import HASHID_FIELD_SALT

from .base import BaseModel


class Comment(BaseModel):
    """Comment model.

    This is useful for the athlete and coach to communicate.

    The `author` is linked to either the coach or athlete model.

    Then, another link exists to either `ProgrammeSession` or the individual \
            `Exercise` of that session.
    """

    reference_id = HashidAutoField(
        primary_key=True, salt=f"comment_{HASHID_FIELD_SALT}"
    )
    content = models.TextField(verbose_name=_("content"))
    author_ct = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            "app_label": "project",
            "model__in": ("coach", "athlete"),
        },
        verbose_name=_("author"),
        related_name="author",
    )
    author_object_id = models.PositiveIntegerField()
    author_content_object = GenericForeignKey("author_ct", "author_object_id")

    location_ct = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            "app_label": "project",
            # TODO: cannot identify programme session
            # "model__in": ("exercise", "programme session"),
        },
        verbose_name=_("location"),
        related_name="location",
    )
    location_object_id = models.PositiveIntegerField()
    location_content_object = GenericForeignKey(
        "location_ct", "location_object_id"
    )

    def __str__(self):
        """Represent string."""
        return self.content[0:20]

    class Meta(BaseModel.Meta):
        """Setting for model.

        Creating an index for the content types.
        """

        indexes = [
            models.Index(fields=["author_ct", "author_object_id"]),
            models.Index(fields=["location_ct", "location_object_id"]),
        ]

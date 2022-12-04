"""ExerciseType model."""

from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _
from hashid_field import HashidAutoField

from config.settings import HASHID_FIELD_SALT
from project.models.base import BaseModel


class ExerciseType(BaseModel):
    """Coaches are able to custom define a new exercise.

    `creator` is the person who created the exercise.

    `contributors` are those who have contributed to the exercise type.

    `is_private` can be flagged to make the exercise private to the creator \
            and contributors.

    Exercises can be tagged and categories to enable easy searching.
    """

    reference_id = HashidAutoField(
        primary_key=True, salt=f"exercisetype_{HASHID_FIELD_SALT}"
    )
    name = models.CharField(_("exercise name"), max_length=25, unique=True)
    description = models.TextField(
        _("exercise description"), blank=True, null=True
    )
    creator = models.ForeignKey(
        "project.Coach",
        on_delete=models.CASCADE,
        verbose_name=_("creator"),
        related_name="exercise_type_creator",
    )
    starred = models.ManyToManyField(
        "project.Coach",
        verbose_name=_("starred"),
        blank=True,
    )
    is_private = models.BooleanField(_("is_private"), default=False)
    categories = models.ManyToManyField(
        "project.ExerciseCategory",
        verbose_name=_("list of categoies"),
        blank=True,
    )

    def get_absolute_url(self):
        """Provide url for the instance."""
        kwargs = {"pk": self.pk}
        return reverse("project:exercise-type-detail", kwargs=kwargs)

    def __str__(self):
        """Represent string."""
        return self.name

    class Meta(BaseModel.Meta):
        """Settings for model."""

        ...

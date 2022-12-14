"""ProgrammeSession model."""

from typing import Iterable

from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from hashid_field import HashidAutoField

from .base import BaseModel
from .managers import ProgrammeSessionManager


class ProgrammeSession(BaseModel):
    """ProgrammeSession is what exercises are programmed for what day.

    The `session_type` is useful if there are multiple sessions in a day.

    The `start` and `end` can be entered by the athlete if they would like to \
            log time at the gym.

    `notes` can provided by the coach for the session.
    """

    class SessionType(models.IntegerChoices):
        """Choices for `session_type`."""

        MORNING = (10, _("Morning"))
        AFTERNOON = (20, _("Afternoon"))
        EVENING = (30, _("Evening"))

    reference_id = HashidAutoField(
        primary_key=True, salt=f"team_{settings.HASHID_FIELD_SALT}"
    )
    coach = models.ForeignKey(
        "project.Coach", on_delete=models.CASCADE, verbose_name=_("coach")
    )
    athlete = models.ForeignKey(
        "project.Athlete", on_delete=models.CASCADE, verbose_name=_("athlete")
    )
    date = models.DateField(_("date"), default=timezone.now())
    session_type = models.IntegerField(
        _("session"),
        choices=SessionType.choices,
        blank=True,
        null=True,
    )

    published = models.DateTimeField(
        _("published"), blank=True, null=True, default=None
    )
    start = models.DateTimeField(
        _("time start of session"),
        blank=True,
        null=True,
    )
    end = models.DateTimeField(
        _("time end of session"),
        blank=True,
        null=True,
    )

    coach_notes = models.TextField(
        _("notes"),
        blank=True,
        null=True,
    )
    comments = GenericRelation(
        "project.Comment",
        related_query_name="programme_session",
        content_type_field="location_ct",
        object_id_field="location_object_id",
    )

    objects = ProgrammeSessionManager()

    @cached_property
    def is_completed(self) -> bool:
        """Marks programme completed."""
        return self.end is not None

    def complete(self):
        """Mark a programme completed."""
        self.end = timezone.now()

    @cached_property
    def is_published(self) -> bool:
        """Mark a programme as published."""
        if self.published is None:
            return False
        return self.published <= timezone.now()

    def publish(self):
        self.published = timezone.now()

    def get_absolute_url(self) -> str:
        """Provide absolute url for the instance."""
        kwargs = {"pk": self.pk}
        return reverse("project:programme-session-detail", kwargs=kwargs)

    def get_hx_edit_url(self) -> str:
        """Provide the edit url for this instance."""
        kwargs = {"pk": self.pk, "athlete_pk": self.athlete.pk}
        return reverse(
            "project:hx-coach-programme-session-update", kwargs=kwargs
        )

    def get_hx_delete_url(self) -> str:
        kwargs = {"pk": self.pk, "athlete_pk": self.athlete.pk}
        return reverse(
            "project:hx-coach-programme-session-delete", kwargs=kwargs
        )

    def get_hx_exercise_new_url(self) -> str:
        """Provide an exercise url for a programme."""
        kwargs = {
            "programme_session_pk": self.pk,
            "athlete_pk": self.athlete.pk,
        }
        return reverse("project:hx-coach-exercise-new", kwargs=kwargs)

    def clean(self, *args, **kwargs):
        pass

    def full_clean(self, *args, **kwargs):
        pass

    def __str__(self) -> str:
        """Represent string."""
        if self.session_type:
            return f"{self.date} - {self.get_session_type_display()}"
        return f"{self.date}"

    class Meta(BaseModel.Meta):
        """Setting for model."""

        ordering: Iterable[str] = ["-date", "-session_type"]

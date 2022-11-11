"""ProgrammeSession model."""

from django.db import models
from django.utils.translation import gettext_lazy as _
from hashid_field import HashidAutoField

from config.settings import HASHID_FIELD_SALT

from .base import BaseModel


class ProgrammeSession(BaseModel):
    """ProgrammeSession is what exercises are programmed for what day.

    The `session_type` is useful if there are multiple sessions in a day.

    The `start` and `end` can be entered by the athlete if they would like to log \
            time at the gym.

    `notes` can provided by the coach for the session.
    """

    class SessionType(models.IntegerChoices):
        """Choices for `session_type`."""

        MORNING = (10, _("Morning"))
        AFTERNOON = (20, _("Afternoon"))
        EVENING = (30, _("Evening"))

    reference_id = HashidAutoField(
        primary_key=True, salt=f"team_{HASHID_FIELD_SALT}"
    )
    coach = models.ForeignKey(
        "project.Coach", on_delete=models.CASCADE, verbose_name=_("coach")
    )
    athlete = models.ForeignKey(
        "project.Athlete", on_delete=models.CASCADE, verbose_name=_("athlete")
    )
    date = models.DateField(
        _("date"),
    )
    session_type = models.IntegerField(
        _("session type"),
        choices=SessionType.choices,
        blank=True,
        null=True,
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
        _("coach's pre training session notes"),
        blank=True,
        null=True,
    )

    def __str__(self):
        """Represent string."""
        if self.session_type:
            return f"{self.date} - {self.session_type}"
        return f"{self.date}"

    class Meta(BaseModel.Meta):
        """Setting for model."""

        ordering = ["-date", "session_type"]

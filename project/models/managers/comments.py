"""Manager for Comments."""

from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime
from typing import TYPE_CHECKING, Union

from django.db import models
from django.db.models import Q

if TYPE_CHECKING:
    from ..athletes import Athlete
    from ..programme_sessions import ProgrammeSession

    GroupByProgrammeSession = dict[Union[QuerySet, list[ProgrammeSession]]]


class CommentQuerySet(models.QuerySet):
    """Comment QuerySet."""

    def unread(self):
        """Provide unread comments."""
        return self.filter(read=False)


class CommentManager(models.Manager):
    """Comment Manager."""

    def get_queryset(self):
        """Redefine."""
        return CommentQuerySet(self.model, using=self._db)

    def unread(self, *args, **kwargs):
        """Unread comments."""
        return self.get_queryset().unread_comments(request)

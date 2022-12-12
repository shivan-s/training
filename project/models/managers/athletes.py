"""Manager for ProgrammeSession."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from ..athletes import Athlete
    from ..programme_sessions import ProgrammeSession


class AthleteQuerySet(models.QuerySet):
    """Queryset for Athlete model."""

    def no_superuser(self) -> QuerySet[Athlete]:
        """Count of athlete, excluding the superuser."""
        return self.filter(user__is_superuser=False)


class AthleteManager(models.Manager):
    """Manager for Athlete model."""

    def get_queryset(self):
        """Reset."""
        return AthleteQuerySet(self.model, using=self._db)

    def count(self, *args, **kwargs) -> int:
        """Count number active users (i.e. not admin)."""
        return qs.get_queryset().no_superuser().count()

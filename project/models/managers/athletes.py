"""Manager for ProgrammeSession."""

from django.db import models


class AthleteManager(models.Manager):
    """Manager for Athlete model."""

    def count(self, *args, **kwargs) -> int:
        """Count number active users (i.e. not admin)."""
        qs = self.get_queryset()
        return qs.filter(user__is_superuser=False).count()

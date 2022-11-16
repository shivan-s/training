"""Manager for ProgrammeSession."""

from django.db import models


class ProgrammeSessionManager(models.Manager):
    """Manager."""

    pass

    # def get_next_by_date(self, reference_id):
    #     """Provide the next instance by date."""
    #     programme_session = ProgrammeSessionManager
    #     Programme.objects.filter

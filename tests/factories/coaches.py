"""Coach factory."""

import factory

from project.models import Coach

from .athletes import AthleteFactory
from .profiles import ProfileFactory


class CoachFactory(factory.django.DjangoModelFactory):
    """Factory."""

    class Meta:
        """Meta."""

        model = Coach

    profile = factory.SubFactory(ProfileFactory)
    athletes = factory.RelatedFactoryList(AthleteFactory, size=20)

"""Athlete factories."""

import factory

from project.models import Athlete

from .coaches import CoachFactory
from .profiles import ProfileFactory


class AthleteFactory(factory.django.DjangoModelFactory):
    """Factory for testing Athletes."""

    class Meta:
        """Meta."""

        model = Athlete

    profile = factory.SubFactory(ProfileFactory)
    coaches = factory.RelatedFactoryList(CoachFactory, size=2)

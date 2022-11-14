"""Athlete factories."""

import factory

from project.models import Athlete


class AthleteFactory(factory.django.DjangoModelFactory):
    """Factory for testing Athletes."""

    class Meta:
        """Meta."""

        model = Athlete

    profile = factory.SubFactory("tests.factories.ProfileFactory")
    coaches = factory.RelatedFactoryList(
        "tests.factories.CoachFactory", size=2
    )

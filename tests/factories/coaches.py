"""Coach factory."""

import factory

from project.models import Coach


class CoachFactory(factory.django.DjangoModelFactory):
    """Factory."""

    class Meta:
        """Meta."""

        model = Coach

    profile = factory.SubFactory("tests.factories.CustomUserFactory")
    athletes = factory.RelatedFactoryList(
        "tests.factories.AthleteFactory", size=20
    )

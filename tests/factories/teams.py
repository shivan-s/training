"""Team factory."""

import factory

from project.models import Team


class TeamFactory(factory.django.DjangoModelFactory):
    """Factory."""

    class Meta:
        """Meta."""

        model = Team

    profile = factory.SubFactory("tests.factories.ProfileFactory")
    athletes = factory.RelatedFactoryList(
        "tests.factories.AthleteFactory", size=20
    )

    name = factory.Faker("company")
    description = factory.Faker("paragraph")
    creator = factory.SubFactory("tests.factories.CoachFactory")
    coaches = factory.RelatedFactoryList(
        "tests.factories.CoachFactory", size=3
    )
    athletes = factory.RelatedFactoryList(
        "tests.factories.AthleteFactory", size=20
    )

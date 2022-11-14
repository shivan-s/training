"""ProgrammeSession factory."""

import factory
import factory.fuzzy

from project.models import ProgrammeSession


class ProgrammeSessionFactory(factory.django.DjangoModelFactory):
    """Factory for testing users."""

    class Meta:
        """Meta."""

        model = ProgrammeSession

    coach = factory.SubFactory("tests.factories.CoachFactory")
    athlete = factory.SubFactory("tests.factories.CoachFactory")
    date = factory.Faker("date")
    session_type = factory.fuzzy.FuzzyChoice(
        ProgrammeSession.SessionType.choices
    )
    start = None
    end = None
    coach_notes = factory.Faker("paragraph")
    exercises = factory.RelatedFactory(
        "tests.factories.Exercise", factory_related_name="exercise", size=3
    )

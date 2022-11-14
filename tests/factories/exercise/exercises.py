"""Exercise factories."""

import factory

from project.models import Exercise


class ExerciseFactory(factory.django.DjangoModelFactory):
    """Factory for testing Profile instances."""

    class Meta:
        """Meta."""

        model = Exercise

    programme_session = factory.SubFactory("tests.factories.ProgrammeSession")
    exercise_type = factory.SubFactory("tests.factories.ExerciseType")
    coach_notes = factory.Faker("paragraph")
    comments = factory.RelatedFactory("tests.factories.Comment", size=10)

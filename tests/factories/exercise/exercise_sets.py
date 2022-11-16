"""ExerciseSet factories."""

import random

import factory

from project.models import ExerciseSet


class ExerciseSetFactory(factory.django.DjangoModelFactory):
    """Factory for testing Profile instances."""

    class Meta:
        """Meta."""

        model = ExerciseSet

    sets = random.randint(1, 5)
    repetitions = random.randint(1, 10)
    weight = random.uniform(1, 100)
    weight_unit = random.choice(ExerciseSet.WeightUnit.choices)
    intended = factory.SubFactory("tests.factories.ExerciseFactory")
    outcome = None

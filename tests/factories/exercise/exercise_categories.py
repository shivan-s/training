"""ExerciseCategory factories."""

import factory

from project.models import ExerciseCategory


class ExerciseCategoryFactory(factory.django.DjangoModelFactory):
    """Factory for testing Profile instances."""

    class Meta:
        """Meta."""

        model = ExerciseCategory

    name = factory.Faker("color_name")
    parent = factory.RelatedFactory("training.ExerciseCategory")

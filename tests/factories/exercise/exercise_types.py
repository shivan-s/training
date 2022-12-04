"""ExerciseType factories."""

import factory

from project.models import ExerciseType


class ExerciseTypeFactory(factory.django.DjangoModelFactory):
    """Factory for testing Profile instances."""

    class Meta:
        """Meta."""

        model = ExerciseType

    programme_session = factory.SubFactory("tests.factories.ProgrammeSession")
    name = factory.Faker("color_name")
    description = factory.Faker("paragraph")
    creator = factory.SubFactory("tests.factories.Coach")
    starred = factory.RelatedFactory("tests.factories.Coach", size=5)
    is_private = factory.Faker("boolean")

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        """Linking to categories."""
        if not create:
            return

        if extracted:
            for group in extracted:
                self.groups.add(group)

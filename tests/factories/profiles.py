"""Profile factories."""

import factory
from django.contrib.auth import get_user_model

from project.models import Profile


class ProfileFactory(factory.django.DjangoModelFactory):
    """Factory for testing Profile instances."""

    class Meta:
        """Meta."""

        model = Profile

    user = factory.SubFactory("tests.factories.CustomUserFactory")
    name = factory.Faker("full_name")
    # TODO : what to do with avatar?
    # avatar = factory.Faker

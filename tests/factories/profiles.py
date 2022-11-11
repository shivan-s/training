"""Profile factories."""

import factory
from django.contrib.admin import get_user_model

from project.Profile
from .users import CustomUserFactory


class ProfileFactory(factory.django.DjangoModelFactory):
    """Factory for testing Profile instances."""

    class Meta:
        """Meta."""

        model = Profile

    user = factory.SubFactory(CustomUserFactory)
    name = factory.Faker("full_name")
    # TODO : what to do with avatar?
    # avatar = factory.Faker

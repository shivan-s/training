"""Users factories."""

import factory
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserFactory(factory.django.DjangoModelFactory):
    """Factory for testing users."""

    class Meta:
        """Meta."""

        model = User

    name = factory.Faker("name")

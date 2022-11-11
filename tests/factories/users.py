"""Users factories."""

import factory
from django.contrib.admin import get_user_model


class CustomUserFactory(factory.django.DjangoModelFactory):
    """Factory for testing users."""

    class Meta:
        """Meta."""

        model = get_user_model()

    email = factory.Faker("email")

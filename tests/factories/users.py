"""Users factories."""

import factory

from users.models import CustomUser


class CustomUserFactory(factory.django.DjangoModelFactory):
    """CustomUser Factory."""

    class Meta:
        """CustomUserFactory settings."""

        model = CustomUser

    username = factory.Faker("user_name")
    name = factory.Faker("name")
    email = factory.Faker("email")

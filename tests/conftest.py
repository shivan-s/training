"""Fixtures and factories."""

import factory.random
import faker.config
import pytest
from django.db import connection
from pytest_factoryboy import register

from .factories import AthleteFactory, CoachFactory, CustomUserFactory

TEST_RANDOM_SEED = 42

faker.config.DEFAULT_LOCALE = "en_NZ"
factory.random.reseed_random(TEST_RANDOM_SEED)

register(CustomUserFactory)
register(AthleteFactory)
register(CoachFactory)


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """Test database setup.

    Installing `pg_trgm` on to the test database, other wise '%' will not be \
            recognised.
    """
    with django_db_blocker.unblock(), connection.cursor() as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")


@pytest.fixture(scope="session")
def authenticated_user(client, django_user_model, custom_user_factory):
    """Create a authenticated user that isn't an admin."""
    user = django_user_model.objects.create_user(
        username=custom_user_factory.username,
        password=custom_user_factory.password,
    )
    return client.force_login(user)

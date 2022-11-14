"""Fixtures and factories."""

import factory.random
import faker.config
import pytest
from django.db import connection
from pytest_factoryboy import register

from .factories import (
    AthleteFactory,
    CoachFactory,
    CustomUserFactory,
    ProfileFactory,
    TeamFactory,
)

TEST_RANDOM_SEED = 42

faker.config.DEFAULT_LOCALE = "en_NZ"
factory.random.reseed_random(TEST_RANDOM_SEED)

register(CustomUserFactory)
register(AthleteFactory)
register(CoachFactory)
register(ProfileFactory)
register(TeamFactory)


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """Test database setup.

    Installing `pg_trgm` on to the test database, other wise '%' will not be \
            recognised.
    """
    with django_db_blocker.unblock(), connection.cursor() as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")


@pytest.fixture
def authenticated_client(client, custom_user):
    """Force login in the custom_user."""
    client.force_login(custom_user)
    return client

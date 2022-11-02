"""Fixtures and factories."""

import factory.random
import faker.config
from pytest_factoryboy import register

from .factories import CustomUserFactory

TEST_RANDOM_SEED = 42

faker.config.DEFAULT_LOCALE = "en_NZ"
factory.random.reseed_random(TEST_RANDOM_SEED)

register(CustomUserFactory)

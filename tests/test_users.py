"""Testing User functionality."""

import json

import pytest
from django.core import serializers
from django.urls import reverse
from pytest_lazyfixture import lazy_fixture

HTTP_200_OK = 200
HTTP_301_MOVED_PERMANENTLY = 301
HTTP_302_FOUND = 302

pytestmark = pytest.mark.django_db


def test_login(client, custom_user):
    """User is able to logout."""
    response = client.post(
        reverse("account_login"),
        json.loads(serializers.serialize("json", [custom_user]))[0],
    )
    assert response.status_code == HTTP_200_OK
    assert response is True
    assert response.user == custom_user


def test_logout(client, custom_user):
    """User is able to logout."""
    response = client.get(reverse("account_logout"))
    assert response.status_code == HTTP_302_FOUND
    assert response.user.is_authenticated is False
    assert response.user != custom_user


@pytest.mark.parametrize(
    "test_client,expected",
    [
        pytest.param(
            lazy_fixture("client"), HTTP_302_FOUND, id="not-logged-in"
        ),
        pytest.param(lazy_fixture("auth_client"), HTTP_200_OK, id="logged-in"),
    ],
)
def test_profile(client, custom_user, test_client, expected):
    """Profile view is only obtainable when logged in."""
    response = test_client.get(reverse("users:profile"))
    assert response.status_code == expected


def test_user_created(client, custom_user_factory):
    response = test_

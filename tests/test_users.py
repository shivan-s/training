"""Testing User functionality."""

import json

import pytest
from django.core import serializers
from django.urls import reverse

HTTP_200_OK = 200

pytestmark = pytest.mark.django_db


def test_login(client, custom_user):
    """User is able to logout."""
    response = client.post(
        reverse("login"),
        json.loads(serializers.serialize("json", [custom_user]))[0],
    )
    assert response.status_code == HTTP_200_OK
    assert response.is_authenticated is True
    assert response.user == custom_user


def test_logout(client, custom_user):
    """User is able to logout."""
    response = client.get(reverse("logout"))
    assert response.status_code == HTTP_200_OK
    assert response.is_authenticated is False
    assert response.user != custom_user

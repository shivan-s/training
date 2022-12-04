"""Testing User functionality."""


from typing import Type

import pytest
from django.contrib.auth import get_user_model
from django.core import serializers
from django.template.response import TemplateResponse
from django.urls import reverse
from pytest_lazyfixture import lazy_fixture

from project.models import Athlete, Coach:

HTTP_200_OK = 200
HTTP_301_MOVED_PERMANENTLY = 301
HTTP_302_FOUND = 302

pytestmark = pytest.mark.django_db


def test_login(client, custom_user):
    """User is able to logout."""
    url = reverse("account_login")
    data = {"email": custom_user.email, "password": custom_user.password}
    response: type[TemplateResponse] = client.post(url, data=data)
    assert response.status_code == HTTP_200_OK
    assert response.context["user"] == data


def test_logout(client, custom_user):
    """User is able to logout."""
    client.force_login(custom_user)
    url = reverse("account_logout")
    response = client.get(url)
    assert response.status_code == HTTP_302_FOUND
    assert response.context["user"] != custom_user


@pytest.mark.parametrize(
    "test_client,expected",
    [
        pytest.param(
            lazy_fixture("client"), HTTP_302_FOUND, id="not-logged-in"
        ),
        pytest.param(
            lazy_fixture("authenticated_client"), HTTP_200_OK, id="logged-in"
        ),
    ],
)
def test_profile(client, custom_user, test_client, expected):
    """Profile view is only obtainable when logged in.

    If the client is not logged in, there will be a redirect to the log in \
            page.
    """
    url = reverse("project:profile")
    response: type[TemplateResponse] = test_client.get(url)
    assert response.status_code == HTTP_200_OK


def test_user_created_signals(client, custom_user_factory, django_user_model):
    """Ensure signals related to user creation work."""

    user = django_user_model.objects.create(
        **custom_user_factory.stub().__dict__
    )
    profile = Profile.objects.filter(user=user)
    assert profile.exists()
    assert Coach.objects.filter(profile=profile.first()).exists()
    assert Athlete.objects.filter(profile=profile.first()).exists()

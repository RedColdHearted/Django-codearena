from http import HTTPStatus

from django.test import Client
from django.urls import reverse

import pytest
from pytest_lazy_fixtures import lf as lazy_fixture

from ...models import User


@pytest.mark.parametrize(
    "client_fixture",
    [
        lazy_fixture("user_client"),
        lazy_fixture("client"),
    ],
)
def test_profile_view(
    client_fixture: Client,
    user: User,
) -> None:
    """Ensure that profile page exists for all users."""
    url = reverse("users:profile", kwargs={"username": user.username})
    response = client_fixture.get(url)

    assert response.status_code == HTTPStatus.OK, response.data

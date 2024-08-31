from http import HTTPStatus

from django.test import Client
from django.urls import reverse

import pytest


@pytest.mark.django_db()
def test_logout_view(
    user_client: Client,
) -> None:
    """Ensure that logout view redirects to login page for all users."""
    url = reverse("users:logout")
    response = user_client.post(url)
    assert response.status_code == HTTPStatus.FOUND, response.content
    assert response.url == reverse("users:login")

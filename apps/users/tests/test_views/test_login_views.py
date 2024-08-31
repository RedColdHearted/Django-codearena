from http import HTTPStatus

from django.test import Client
from django.urls import reverse

from ...factories import UserFactory


def test_login_view(
    client: Client,
) -> None:
    """Ensure that the login works for an existing user."""
    user = UserFactory()
    login_data = {
        "username": user.email,
        "password": "Test111!",
    }
    url = reverse("users:login")
    response = client.post(url, login_data)
    assert response.status_code == HTTPStatus.FOUND, response.content
    assert response.wsgi_request.user.is_authenticated

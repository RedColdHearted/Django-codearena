from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

import pytest

User = get_user_model()


@pytest.mark.django_db()
def test_signup_view(
    client: Client,
) -> None:
    """Ensure that signup creates a new user."""
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password1": "Test111!",
        "password2": "Test111!",
    }
    url = reverse("users:signup")
    response = client.post(url, user_data)

    assert response.status_code == HTTPStatus.FOUND, response.content
    assert User.objects.filter(username="newuser").exists()

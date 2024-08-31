from http import HTTPStatus

from django.test import Client
from django.urls import reverse

from ...models import User


def test_profile_update_view(
    client: Client,
    user: User,
) -> None:
    """Ensure that the profile update works for an existing user."""
    client.force_login(user)

    updated_data = {
        "username": "Updated_username",
        "first_name": "Updated_name",
        "last_name": "Updated_last_name",
        "email": "Updated@email.com",
    }
    response = client.post(
        reverse("users:update"),
        updated_data,
    )
    user.refresh_from_db()
    assert response.status_code == HTTPStatus.FOUND, response.data
    for key, value in updated_data.items():
        assert getattr(user, key) == value

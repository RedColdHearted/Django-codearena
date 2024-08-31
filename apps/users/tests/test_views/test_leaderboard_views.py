from http import HTTPStatus

from django.test import Client
from django.urls import reverse

import pytest
from pytest_lazy_fixtures import lf as lazy_fixture

from apps.issues.models import SolvedIssue


@pytest.mark.parametrize(
    "client_fixture",
    [
        lazy_fixture("user_client"),
        lazy_fixture("client"),
    ],
)
def test_leaderboard_view(
    client_fixture: Client,
    solved_issue_with_user: SolvedIssue,
) -> None:
    """Ensure that leaders board page exists and contain data for all users."""
    url = reverse("users:leaderboard")
    response = client_fixture.get(url)
    assert response.status_code == HTTPStatus.OK, response.data
    assert solved_issue_with_user.user in response.context["user_list"]

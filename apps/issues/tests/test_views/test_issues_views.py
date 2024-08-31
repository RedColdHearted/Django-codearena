import http

from django.test import Client
from django.urls import reverse

import pytest
from pytest_mock import MockerFixture

from apps.users.models import User

from ... import models
from .. import shortcuts


def test_issues_view(
    client: Client,
) -> None:
    """Ensure that issues list page exists."""
    url = reverse("issues:issues")
    response = client.get(url)

    assert response.status_code == http.HTTPStatus.OK, response.data


def test_issue_detail_view(
    user_client: Client,
    issue: models.Issue,
) -> None:
    """Ensure that user can get page with issue details."""
    url = shortcuts.get_issue_solve_url(issue.id)

    response = user_client.get(url)
    assert response.context["issue"] == issue
    assert response.status_code == http.HTTPStatus.OK, response.data


def test_unauthorized_user_cant_get_issue_detail_page(
    client: Client,
    issue: models.Issue,
) -> None:
    """Ensure that unauthorized user can't access to page."""
    url = shortcuts.get_issue_solve_url(issue.id)

    response = client.get(url)
    assert response.status_code == http.HTTPStatus.FOUND, response.data


@pytest.mark.parametrize(
    ["data", "is_exist", "response_status"],
    [
        [
            {
                "language": models.constants.Languages.PYTHON,
                "content": "",
            },
            False,
            http.HTTPStatus.OK,
        ],
        [
            {
                "language": models.constants.Languages.PYTHON,
                "content": "def foo(a: str, b: float):/n    return 123",
            },
            True,
            http.HTTPStatus.OK,
        ],
    ],
)
def test_issue_detail_view_create_solution(
    user: User,
    user_client: Client,
    issue: models.Issue,
    data: list[dict[str, str]],
    is_exist: bool,
    response_status: http.HTTPStatus,
    mocker: MockerFixture,
) -> None:
    """Ensure that user can create a solution trough issue details page."""
    url = shortcuts.get_issue_solve_url(issue.id)

    # mocking docker test cases run functionality
    mocker.patch(
        "apps.issues.tasks.run_solution_tests",
        return_value=None,
    )
    response = user_client.post(
        url,
        data,
        follow=True,
    )
    assert response.status_code == response_status


def test_issue_like(
    user_client: Client,
    issue: models.Issue,
    user: User,
):
    """Ensure that user can like issue."""
    response = user_client.post(
        shortcuts.get_issue_like_url(issue.id),
    )

    assert response.status_code == http.HTTPStatus.CREATED
    json_data = response.json()
    assert json_data.get("status") == http.HTTPStatus.CREATED
    assert json_data.get("is_liked")
    assert issue.likes.filter(id=user.id).exists()


def test_issue_unlike(
    user_client: Client,
    issue: models.Issue,
    user: User,
):
    """Ensure that user can unlike issue."""
    issue.likes.add(user)

    response = user_client.post(
        shortcuts.get_issue_like_url(issue.id),
    )

    assert response.status_code == http.HTTPStatus.CREATED
    json_data = response.json()
    assert json_data.get("status") == http.HTTPStatus.CREATED
    assert not json_data.get("is_liked")
    assert not issue.likes.filter(id=user.id).exists()


def test_issue_like_user_not_authenticated(
    client: Client,
    issue: models.Issue,
):
    """Ensure that not authenticated user can't like issue."""
    response = client.post(shortcuts.get_issue_like_url(issue.id))

    assert response.status_code == http.HTTPStatus.FORBIDDEN
    json_data = response.json()
    assert json_data.get("status") == http.HTTPStatus.FORBIDDEN
    assert json_data.get("detail") == (
        "Only authenticated user can like issues"
    )

from django.test import Client

from rest_framework import test

import pytest
import pytest_django

from apps.issues.factories import SolvedIssueFactory
from apps.issues.models import SolvedIssue
from apps.issues.models.constants import Complexity
from apps.users.factories import UserFactory
from apps.users.models import User


@pytest.fixture
def api_client() -> test.APIClient:
    """Create api client."""
    return test.APIClient()


@pytest.fixture
def user(
    django_db_blocker: pytest_django.DjangoDbBlocker,
) -> User:
    """Create common user."""
    with django_db_blocker.unblock():
        return UserFactory()


@pytest.fixture
def multiple_users(
    django_db_blocker: pytest_django.DjangoDbBlocker,
) -> list[User]:
    """Create multiple users."""
    with django_db_blocker.unblock():
        return UserFactory.create_batch(3)


@pytest.fixture
def multiple_solved_issue_with_users(
    django_db_blocker: pytest_django.DjangoDbBlocker,
    multiple_users: list[User],
) -> list[SolvedIssue]:
    """Create multiple users."""
    with django_db_blocker.unblock():
        return [
            SolvedIssueFactory.create(
                user=user,
                issue__complexity=complexity,
            )
            for user, complexity in zip(
                multiple_users,
                Complexity.values,
                strict=True,
            )
        ]


@pytest.fixture
def admin_user(
    django_db_blocker: pytest_django.DjangoDbBlocker,
) -> User:
    """Create admin user."""
    with django_db_blocker.unblock():
        return UserFactory(
            is_staff=True,
            is_superuser=True,
        )


@pytest.fixture
def solved_issue_with_user(
    django_db_blocker: pytest_django.DjangoDbBlocker,
    user: User,
) -> SolvedIssue:
    """Create admin user."""
    with django_db_blocker.unblock():
        return SolvedIssueFactory(user=user)


@pytest.fixture
def user_api_client(
    api_client: test.APIClient,
    user: User,
) -> test.APIClient:
    """Authenticate user and return API client."""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_api_client(
    api_client: test.APIClient,
    admin_user: User,
) -> test.APIClient:
    """Authenticate admin user and return API client."""
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def user_client(
    client: Client,
    user: User,
) -> Client:
    """Return client for basic user."""
    client.force_login(user)
    return client


@pytest.fixture
def admin_client(
    client: Client,
    admin_user: User,
) -> Client:
    """Return client for admin user."""
    client.force_login(admin_user)
    return client


@pytest.fixture(scope="module")
def django_client() -> Client:
    """Module-level fixture of django client."""
    return Client()

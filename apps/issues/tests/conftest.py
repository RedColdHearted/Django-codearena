import pytest
import pytest_django

from .. import factories, models


@pytest.fixture(scope="module")
def issue(
    django_db_blocker: pytest_django.DjangoDbBlocker,
) -> models.Issue:
    """Create Issue instance for testing."""
    with django_db_blocker.unblock():
        return factories.IssueFactory()


@pytest.fixture(scope="module")
def solution(
    django_db_blocker: pytest_django.DjangoDbBlocker,
) -> models.Issue:
    """Create Solution instance for testing."""
    with django_db_blocker.unblock():
        return factories.SolutionFactory()

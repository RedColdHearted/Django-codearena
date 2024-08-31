from django.contrib.auth import get_user_model

from .. import models

User = get_user_model()


def retrieve_last_solution(
    user: User,  # pyright: ignore
    issue: models.Issue,
) -> models.Solution | None:
    """Return user's last issue solution."""
    return (
        models.Solution.objects.filter(
            user=user,
            issue=issue,
        )
        .order_by("-created")
        .first()
    )

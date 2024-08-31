from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class SolvedIssue(BaseModel):
    """Represent codearena's SolvedIssue in db."""

    user = models.ForeignKey(
        to="users.User",
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="solved_issues",
    )
    issue = models.ForeignKey(
        to="issues.Issue",
        verbose_name=_("Issue"),
        on_delete=models.CASCADE,
        related_name="solved_issues",
    )

    class Meta:
        verbose_name = _("Solved issue by user")
        verbose_name_plural = _("Solved issues by users")

    def __str__(self) -> str:
        return f"SolvedIssue(User={self.user.id}, Issue={self.issue.id})"

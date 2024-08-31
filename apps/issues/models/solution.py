from django.core.validators import DecimalValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel

from . import constants


class Solution(BaseModel):
    """Represent codearena's solution in db."""

    user = models.ForeignKey(
        to="users.User",
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="solutions",
    )
    issue = models.ForeignKey(
        to="issues.Issue",
        verbose_name=_("Issue"),
        on_delete=models.CASCADE,
        related_name="solutions",
    )
    language = models.CharField(
        choices=constants.Languages.choices,
        verbose_name=_("Language"),
        max_length=30,
    )
    content = models.TextField(
        verbose_name=_("Content"),
    )
    average_time_usage = models.FloatField(
        verbose_name=_("Time usage"),
        validators=[
            DecimalValidator(1, 10),
        ],
        null=True,
    )
    average_memory_usage = models.FloatField(
        verbose_name=_("Memory usage"),
        validators=[
            DecimalValidator(1, 10),
        ],
        null=True,
    )
    testing_status = models.CharField(
        choices=constants.SolutionStatus.choices,
        verbose_name=_("Solution status"),
        default=constants.SolutionStatus.PENDING,
        max_length=15,
    )

    class Meta:
        verbose_name = _("Solution")
        verbose_name_plural = _("Solutions")

    def __str__(self) -> str:
        return f"Solution(User={self.user.id}, Issue={self.issue.id})"

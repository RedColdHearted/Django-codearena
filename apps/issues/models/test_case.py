from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel

from . import constants


class TestCase(BaseModel):
    """Represent issue's test case in db."""

    issue = models.ForeignKey(
        to="issues.Issue",
        verbose_name=_("Issue id"),
        on_delete=models.CASCADE,
        related_name="test_cases",
    )
    language = models.CharField(
        choices=constants.Languages.choices,
        default=constants.Languages.PYTHON,
        verbose_name=_("Language"),
        max_length=30,
    )
    input_data = models.TextField(
        verbose_name=_("Input data"),
    )
    excepted_output = models.TextField(
        verbose_name=_("Excepted output"),
    )
    order = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
    )
    allocated_time = models.IntegerField(
        verbose_name=_("Allocated time(seconds)"),
        validators=[
            MinValueValidator(3),
            MaxValueValidator(6),
        ],
    )
    allocated_memory = models.IntegerField(
        verbose_name=_("Allocated memory(mb)"),
        default=128,
        validators=[
            MinValueValidator(8),
            MaxValueValidator(256),
        ],
    )

    class Meta:
        verbose_name = _("Test case")
        verbose_name_plural = _("Test cases")
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "issue",
                    "order",
                ),
                name="unique_task_order",
            ),
        ]

    def __str__(self) -> str:
        return (
            f"TestCase(issue_id={self.issue.id}, language={self.language}, "
            f"order={self.order})"
        )

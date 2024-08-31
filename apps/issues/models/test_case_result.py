from django.core.validators import (
    DecimalValidator,
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel

from . import constants


class TestCaseResult(BaseModel):
    """Represent codearena's TestCaseResult in db."""

    solution = models.ForeignKey(
        to="issues.Solution",
        verbose_name=_("Solution"),
        on_delete=models.CASCADE,
        related_name="test_cases_results",
    )
    test_case = models.ForeignKey(
        to="issues.TestCase",
        verbose_name=_("Test case"),
        on_delete=models.CASCADE,
        related_name="test_cases_results",
    )
    status = models.CharField(
        choices=constants.TestResultStatus.choices,
        verbose_name=_("Status"),
        max_length=10,
    )
    execution_log = models.TextField(
        verbose_name=_("Execution log"),
        help_text=_("This field contains output of executed test case"),
        blank=True,
    )
    time_used = models.FloatField(
        verbose_name=_("Time used"),
        validators=[
            DecimalValidator(1, 3),
            MinValueValidator(0.1),
            MaxValueValidator(6.1),
        ],
        null=True,
    )
    memory_used = models.FloatField(
        verbose_name=_("Memory used"),
        validators=[
            DecimalValidator(3, 1),
            MinValueValidator(1),
            MaxValueValidator(256),
        ],
        null=True,
    )

    class Meta:
        verbose_name = _("Test case result")
        verbose_name_plural = _("Test case results")

    def __str__(self) -> str:
        return (
            f"TestCaseResult(TestCase={self.test_case.id}, "
            f"status={self.status})"
        )

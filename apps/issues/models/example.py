from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Example(BaseModel):
    """Represent codearena's example for issue in db.

    Contains examples of code in a pseudo-language for a better
    understanding of Issue.

    """

    issue = models.ForeignKey(
        to="issues.Issue",
        verbose_name=_("Issue"),
        on_delete=models.CASCADE,
        related_name="examples",
    )
    input = models.TextField(
        verbose_name=_("Input"),
    )
    output = models.TextField(
        verbose_name=_("Output"),
    )
    explanation = models.TextField(
        verbose_name=_("Explanation"),
        blank=True,
    )
    order = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
    )

    class Meta:
        verbose_name = _("Example")
        verbose_name_plural = _("Examples")
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "issue",
                    "order",
                ),
                name="unique_example_order",
            ),
        ]

    def __str__(self) -> str:
        return f"Example(Issue={self.issue.id}, order={self.order})"

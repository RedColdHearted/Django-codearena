from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel

from . import constants


class Issue(BaseModel):
    """Represent codearena's issue in db."""

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=50,
    )
    description = models.TextField(
        verbose_name=_("Description"),
    )
    hint = models.TextField(
        verbose_name=_("Hint"),
        help_text=_(
            "A hint that will push the user towards solving the issue",
        ),
        blank=True,
    )
    complexity = models.CharField(
        choices=constants.Complexity.choices,
        verbose_name=_("Complexity"),
        help_text=_(
            "Levels that are associated with the difficulty "
            "of finding a solution",
        ),
        max_length=15,
    )
    tags = models.ManyToManyField(
        to="issues.Tag",
        verbose_name=_("Issue tags"),
        help_text=_("Tags that attached with issue"),
        related_name="issues",
    )
    likes = models.ManyToManyField(
        to="users.User",
        verbose_name=_("Issue likes"),
        help_text=_("User's likes to issue"),
        related_name="issues",
        blank=True,
    )

    class Meta:
        verbose_name = _("Issue")
        verbose_name_plural = _("Issues")

    def __str__(self) -> str:
        return self.title

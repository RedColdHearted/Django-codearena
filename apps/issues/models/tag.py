from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Tag(BaseModel):
    """Represent codearena's tag for issue in db."""

    title = models.CharField(
        verbose_name=_("Tag title"),
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self) -> str:
        return self.title

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from imagekit import models as imagekitmodels
from imagekit.processors import ResizeToFill, Transpose

from apps.core.models import BaseModel


class Achievement(
    BaseModel,
):
    """Represent codearena's achievement in db."""

    title = models.CharField(
        unique=True,
        verbose_name=_("Achievement"),
        max_length=55,
    )
    description = models.TextField(
        verbose_name="Description",
    )
    image = imagekitmodels.ProcessedImageField(
        verbose_name=_("Achievement image"),
        blank=True,
        null=True,
        upload_to=settings.DEFAULT_MEDIA_PATH,
        max_length=512,
        processors=[Transpose()],
        options={
            "quality": 100,
        },
    )
    image_thumbnail = imagekitmodels.ImageSpecField(
        source="image",
        processors=[
            ResizeToFill(50, 50),
        ],
    )

    class Meta:
        verbose_name = _("Achievement")
        verbose_name_plural = _("Achievements")

    def __str__(self) -> str:
        return self.title

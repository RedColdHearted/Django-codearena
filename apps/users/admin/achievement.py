from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from imagekit.admin import AdminThumbnail

from apps.core.admin import BaseAdmin

from ..models import Achievement


@admin.register(Achievement)
class AchievementAdmin(BaseAdmin):
    """UI for Achievement model."""

    ordering = (
        "title",
    )
    image_thumbnail = AdminThumbnail(image_field="image_thumbnail")
    list_display = (
        "image_thumbnail",
        "title",
        "description",
    )
    list_display_links = (
        "title",
    )
    search_fields = (
        "title",
    )
    add_fieldsets = (
        (
            None, {
                "classes": ("wide",),
                "fields": (
                    "title",
                    "description",
                ),
            },
        ),
    )
    fieldsets = (
        (
            None, {
                "fields": (
                    "title",
                ),
            },
        ),
        (
            _("Description"), {
                "fields": (
                    "description",
                    "image",
                ),
            },
        ),
    )

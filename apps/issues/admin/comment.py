from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.core.admin import BaseAdmin

from .. import models


@admin.register(models.Comment)
class CommentAdmin(BaseAdmin):
    """UI for Comment model."""

    ordering = ("id",)
    autocomplete_fields = (
        "user",
    )
    filter_horizontal = (
        "likes",
    )
    list_display = (
        "id",
        "user",
        "object_id",
        "content_type",
    )
    list_display_links = (
        "id",
        "user",
        "object_id",
        "content_type",
    )
    search_fields = (
        "id",
        "user",
    )
    fieldsets = (
        (
            _("Main Info"), {
                "fields": (
                    "user",
                    "content",
                    "likes",
                    "object_id",
                    "content_type",
                ),
            },
        ),
    )

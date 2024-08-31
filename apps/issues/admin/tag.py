from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.core.admin import BaseAdmin

from .. import models


@admin.register(models.Tag)
class TagAdmin(BaseAdmin):
    """UI for Tag model."""

    ordering = ("id",)
    list_display = (
        "id",
        "title",
    )
    list_display_links = (
        "id",
    )
    search_fields = (
        "id",
        "title",
    )
    add_fieldsets = (
        (
            None, {
                "classes": ("wide",),
                "fields": (
                    "title",
                ),
            },
        ),
    )
    fieldsets = (
        (
            _("Main Info"), {
                "fields": (
                    "title",
                ),
            },
        ),
    )

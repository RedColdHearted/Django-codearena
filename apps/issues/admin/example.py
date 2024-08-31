from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.core.admin import BaseAdmin

from .. import models


@admin.register(models.Example)
class ExampleAdmin(BaseAdmin):
    """UI for Example model."""

    ordering = ("id",)
    autocomplete_fields = (
        "issue",
    )
    list_display = (
        "id",
        "issue",
        "order",
    )
    list_display_links = (
        "id",
        "issue",
        "order",
    )
    search_fields = (
        "id",
        "issue",
        "order",
    )
    fieldsets = (
        (
            _("Main Info"), {
                "fields": (
                    "issue",
                    "input",
                    "output",
                    "explanation",
                    "order",
                ),
            },
        ),
    )

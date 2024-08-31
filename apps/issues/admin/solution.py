from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.core.admin import BaseAdmin

from .. import models


@admin.register(models.Solution)
class SolutionAdmin(BaseAdmin):
    """UI for Solution model."""

    ordering = ("id",)
    autocomplete_fields = (
        "user",
        "issue",
    )
    list_display = (
        "id",
        "user",
        "issue",
    )
    list_display_links = (
        "id",
        "issue",
        "user",
    )
    search_fields = (
        "id",
        "issue",
        "user",
    )
    fieldsets = (
        (
            _("Main Info"), {
                "fields": (
                    "user",
                    "issue",
                    "language",
                    "content",
                    "average_time_usage",
                    "average_memory_usage",
                    "testing_status",
                ),
            },
        ),
    )

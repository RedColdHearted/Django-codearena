from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.core.admin import BaseAdmin

from .. import models


@admin.register(models.TestCaseResult)
class TestCaseResultAdmin(BaseAdmin):
    """UI for TestCaseResult model."""

    ordering = ("id",)
    autocomplete_fields = (
        "test_case",
    )
    list_display = (
        "id",
        "test_case",
        "status",
    )
    list_display_links = (
        "id",
        "test_case",
    )
    search_fields = (
        "id",
        "test_case",
    )
    fieldsets = (
        (
            _("Main Info"), {
                "fields": (
                    "test_case",
                    "status",
                    "execution_log",
                    "time_used",
                    "memory_used",
                ),
            },
        ),
    )

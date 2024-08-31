from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.core.admin import BaseAdmin

from .. import models


@admin.register(models.TestCase)
class TestCaseAdmin(BaseAdmin):
    """UI for TestCase model."""

    ordering = ("id",)
    autocomplete_fields = (
        "issue",
    )
    list_display = (
        "id",
        "issue",
        "language",
    )
    list_display_links = (
        "id",
        "issue",
        "language",
    )
    search_fields = (
        "id",
        "issue",
        "language",
    )
    add_fieldsets = (
        (
            None, {
                "classes": (
                    "wide",
                ),
                "fields": (
                    "name",
                ),
            },
        ),
    )
    fieldsets = (
        (
            _("Main Info"), {
                "fields": (
                    "issue",
                    "language",
                    "input_data",
                    "excepted_output",
                    "order",
                    "allocated_time",
                    "allocated_memory",
                ),
            },
        ),
    )

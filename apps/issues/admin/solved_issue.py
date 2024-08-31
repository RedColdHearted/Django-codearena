from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.core.admin import BaseAdmin

from .. import models


@admin.register(models.SolvedIssue)
class SolvedIssueAdmin(BaseAdmin):
    """UI for SolvedIssue model."""

    ordering = (
        "user",
    )
    list_display = (
        "user",
        "issue",
        "created",
    )
    list_display_links = (
        "user",
        "issue",
    )
    search_fields = (
        "user",
        "issue",
    )
    add_fieldsets = (
        (
            None, {
                "classes": ("wide",),
                "fields": (
                    "user",
                    "issue",
                ),
            },
        ),
    )
    fieldsets = (
        (
            _("Main Info"), {
                "fields": (
                    "user",
                    "issue",
                ),
            },
        ),
    )

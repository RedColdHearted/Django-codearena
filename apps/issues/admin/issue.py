from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.core.admin import BaseAdmin

from .. import models
from . import inlines


@admin.register(models.Issue)
class IssueAdmin(BaseAdmin):
    """UI for Issue model."""

    inlines = (
        inlines.ExampleInline,
        inlines.TestCaseInline,
    )
    ordering = (
        "id",
    )
    filter_horizontal = (
        "tags",
    )
    list_display = (
        "id",
        "title",
    )
    list_display_links = (
        "id",
        "title",
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
                    "hint",
                    "tags",
                    "complexity",
                ),
            },
        ),
    )
    fieldsets = (
        (
            _("Main Info"), {
                "fields": (
                    "title",
                    "description",
                    "hint",
                    "tags",
                    "complexity",
                ),
            },
        ),
    )

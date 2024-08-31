from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class IssuesAppConfig(AppConfig):
    """Default configuration for Issues app."""

    name = "apps.issues"
    verbose_name = _("Issues")

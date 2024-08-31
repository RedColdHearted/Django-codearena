from django.contrib import admin
from django.urls import include, path

from apps.core.views import IndexView
from libs.health_checks import liveness_check

from .api_versions import urlpatterns as api_urlpatterns
from .debug import urlpatterns as debug_urlpatterns

urlpatterns = [
    path(
        "",
        IndexView.as_view(),
        name="index",
    ),
    path(
        "mission-control-center/",
        admin.site.urls,
    ),
    path(
        "issues/",
        include("apps.issues.urls"),
    ),
    path(
        "users/",
        include("apps.users.urls"),
    ),
    # Django Health Check url
    # See more details: https://pypi.org/project/django-health-check/
    # Custom checks at lib/health_checks
    # TODO: Remove old aliases (`health` and `liveness`) after 2024-09-01  # noqa: E501, TD002, TD003
    path(
        "health/",
        include(
            "health_check.urls",
            namespace="health",
        ),
        name="health",
    ),
    path(
        "liveness/",
        liveness_check.liveness_check,
        name="liveness",
    ),
    path(
        "healthz/",
        include(
            "health_check.urls",
            namespace="healthz",
        ),
        name="healthz",
    ),
    path(
        "livez/",
        liveness_check.liveness_check,
        name="livez",
    ),
    path(
        "readyz/",
        liveness_check.liveness_check,
        name="readyz",
    ),
]

urlpatterns += api_urlpatterns
urlpatterns += debug_urlpatterns

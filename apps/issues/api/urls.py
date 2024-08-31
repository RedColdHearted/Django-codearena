from django.urls import path

from . import views

urlpatterns = [
    path(
        "test-case-result/<int:solution_id>/",
        views.TestCaseResultViewSet.as_view(
            {
                "get": "list",
            },
        ),
        name="test-case-result-by-solution",
    ),
]

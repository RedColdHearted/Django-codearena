from django.urls import path

from . import views

app_name = "issues"

urlpatterns = [
    path(
        "",
        views.IssueListView.as_view(),
        name="issues",
    ),
    path(
        "<int:pk>/",
        views.IssueSolveView.as_view(),
        name="issue-solve",
    ),
    path(
        "<int:pk>/like/",
        views.IssueLikeView.as_view(),
        name="issue-like",
    ),
]

from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)
from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path(
        "profile/<str:username>/",
        views.ProfileView.as_view(),
        name="profile",
    ),
    path(
        "update/",
        views.ProfileUpdateView.as_view(),
        name="update",
    ),
    path(
        "signup/",
        views.SignUpView.as_view(),
        name="signup",
    ),
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),
    path(
        "login/",
        LoginView.as_view(
            template_name="users/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path(
        "leaderboard/",
        views.LeaderBoardView.as_view(),
        name="leaderboard",
    ),
]

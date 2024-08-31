from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models.base import Model
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from ..forms import UserRegistrationForm, UserUpdateForm
from ..models import User
from .constants import (
    COUNT_OF_TOP_USERS,
    PROFILE_ACTIVITY_PAGINATION,
)


class ProfileView(DetailView):
    """View of user profile."""

    model = User
    template_name = "users/profile.html"
    context_object_name = "user"
    queryset = User.objects.with_solved_issues()

    def get_object(self) -> Model:
        """Return the user object based on the username provided in the URL.

        The method has been overridden to allow searching
        for users regardless of case sensitivity.
        This ensures that the username lookup does not
        differentiate between uppercase and lowercase letters
        Method performs annotate rank: Assigns a rank to each user based on
            their position in the sorted queryset.

        """
        username = slugify(self.kwargs.get("username"))
        queryset = super().get_queryset()
        return queryset.users_rank().get(username__iexact=username)

    def get_context_data(self, **kwargs):
        """Prepare data about solved issues to context."""
        context = super().get_context_data(**kwargs)
        user = self.object
        solved_issues = user.solved_issues.order_by("id")
        paginator = Paginator(solved_issues, PROFILE_ACTIVITY_PAGINATION)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["page_obj"] = page_obj

        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """View for update user profile."""

    template_name = "users/update.html"
    form_class = UserUpdateForm

    def get_object(self, *args, **kwargs):
        """Return user object."""
        return self.request.user

    def get_success_url(self):
        """Return URL to redirect after form submission."""
        username = self.request.user.username
        return reverse_lazy(
            "users:profile",
            args=(
                username,
            ),
        )


class SignUpView(CreateView):
    """View for signing up."""

    form_class = UserRegistrationForm
    success_url = reverse_lazy("users:login")
    template_name = "users/signup.html"


class LeaderBoardView(ListView):
    """View for leaderboard."""

    model = User
    template_name = "users/leaderboard.html"
    queryset = User.objects.with_solved_issues()[:COUNT_OF_TOP_USERS]
    paginate_by = 10

    def get_queryset(self):
        """Return queryset with rank annotate."""
        queryset = super().get_queryset()
        return queryset.users_rank()

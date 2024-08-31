import http

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.base import Model as Model
from django.http import (
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import CreateView, DetailView

from django_filters.views import FilterView

from .. import filters, forms, models, services

User = get_user_model()


class IssueListView(FilterView):
    """Issue list view."""

    paginate_by = 10
    template_name = "issues/issues.html"
    model = models.Issue
    filterset_class = filters.IssueFilter
    context_object_name = "issues"

class IssueSolveView(LoginRequiredMixin, DetailView, CreateView):
    """View that provides feature to solve issue."""

    model = models.Issue
    template_name = "issues/issue-solve.html"
    context_object_name = "issue"
    form_class = forms.SolutionCreateForm
    queryset = models.Issue.objects.all()

    def get_success_url(self):
        """Return success url."""
        return reverse_lazy(
            "issues:issue-solve",
            args=(
                self.object.pk,
            ),
        )

    def get_form_kwargs(self):
        """Prepare data to form's kwargs."""
        kwargs = super().get_form_kwargs()
        user = self.request.user
        issue = self.object
        kwargs["user"] = user
        kwargs["issue"] = issue
        kwargs["instance"] = services.issue.retrieve_last_solution(
            user,
            issue,
        )
        return kwargs

    def get_context_data(self, **kwargs):
        """Prepare page context."""
        issue = self.object
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context["issue"] = issue
        context["form"] = self.form_class(user, issue)
        context["examples"] = models.Example.objects.filter(
            issue=issue,
        ).order_by("order")
        solution = services.issue.retrieve_last_solution(
            user,
            issue,
        )
        context["is_liked"] = issue.likes.filter(id=user.id).exists()
        context["solution"] = solution
        context["test_case_results"] = models.TestCaseResult.objects.filter(
            solution=solution,
        ).order_by("created")
        return context

    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        self.object = self.get_object()
        return super().get_initial()

    def form_valid(self, form):
        """If the form is valid, save it."""
        form.save()
        return HttpResponseRedirect(self.get_success_url())

class IssueLikeView(View):
    """View to like/unlike issue."""

    def post(self, request, *args, **kwargs):
        """Perform add or remove issue like."""
        issue = get_object_or_404(
            models.Issue,
            id=kwargs["pk"],
        )
        user = request.user
        if not user.is_authenticated:
            return JsonResponse(
                {
                    "status": http.HTTPStatus.FORBIDDEN,
                    "detail": _("Only authenticated user can like issues"),
                },
                status=http.HTTPStatus.FORBIDDEN,
            )
        is_liked = False
        if issue.likes.filter(id=user.id).exists():
            issue.likes.remove(user)
        else:
            issue.likes.add(user)
            is_liked = True
        return JsonResponse(
            {
                "status": http.HTTPStatus.CREATED,
                "detail": _(f"Issue {"un" if not is_liked else ""}liked"),
                "is_liked": is_liked,
            },
            status=http.HTTPStatus.CREATED,
        )

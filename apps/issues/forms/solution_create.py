from django import forms

from apps.users.models import User

from .. import models, tasks


class SolutionCreateForm(forms.ModelForm):
    """Represent solution form."""

    language = forms.ChoiceField(
        choices=models.constants.Languages.choices,
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "language-select",
                "data-placeholder": "Select a tag",
            },
        ),
    )
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "id": "code-input",
                "rows": "10",
            },
        ),
    )

    class Meta:
        model = models.Solution
        fields = (
            "language",
            "content",
        )

    def __init__(
        self,
        user: User,
        issue: models.Issue,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.user = user
        self.issue = issue

    def save(self, commit: bool = True) -> models.Solution:
        """Save this form's self.instance or return old one.

        Old instance will returned if it exists and has
        `PENDING` or `IN_PROGRESS` status, if there is no one, a new one will
        be created with started celery task that performs tests.

        """
        old_instance = models.Solution.objects.filter(
            user=self.user,
            issue=self.issue,
        ).first()
        if old_instance and old_instance.testing_status in (
            models.constants.SolutionStatus.PENDING,
            models.constants.SolutionStatus.IN_PROGRESS,
        ):
            return old_instance
        instance = super().save(commit=False)
        instance.user = self.user
        instance.issue = self.issue
        if commit:
            instance.save()
            tasks.run_solution_tests.delay(solution_id=instance.id)
        return instance

from django import forms

from django_filters import filterset

from .. import models


class IssueFilter(filterset.FilterSet):
    """Represent filter of issues list."""

    title = filterset.CharFilter(
        lookup_expr="icontains",
        label="Issue title",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter task name",
            },
        ),
    )
    tags = filterset.ModelChoiceFilter(
        queryset=models.Tag.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "data-placeholder": "Select a tag",
            },
        ),
        required=False,
    )

    class Meta:
        model = models.Issue
        fields = (
            "title",
            "tags",
        )

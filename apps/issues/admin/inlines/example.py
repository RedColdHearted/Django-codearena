from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ... import models


class ExampleInlineFormSet(forms.BaseInlineFormSet):
    """Form set for inline of Example.

    This inline need to validate that at least one instance of "Example" was
    creating during creating issue.

    """

    def clean(self) -> None:
        """Validate there is at least one example on the form."""
        super().clean()
        if not any(form.cleaned_data for form in self.forms):
            raise forms.ValidationError(
                _("You must create at least one example"),
            )

class ExampleInline(admin.TabularInline):
    """UI inline of Example for Issue panel.

    extra: Returns the maximum number of extra inline forms to use.
    https://shorturl.at/DB6cw

    """

    model = models.Example
    formset = ExampleInlineFormSet
    extra = 1

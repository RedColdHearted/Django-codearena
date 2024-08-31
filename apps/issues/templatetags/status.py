from django import template

from .. import models
from ..models.constants import TestResultStatus

register = template.Library()


@register.filter
def status(test_case_result: models.TestCaseResult) -> str:
    """Generate message tag about test case result status."""
    statuses = {
        TestResultStatus.COMPLETE: ("Correct Result", "text-success"),
        TestResultStatus.FAIL: ("Incorrect Result", "text-warning"),
        TestResultStatus.ERROR: ("An error has occurred", "text-danger"),
    }
    message, style_class = statuses[test_case_result.status]

    return f"<strong class='{style_class}'>{message}</strong>"

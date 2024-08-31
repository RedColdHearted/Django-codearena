from django.db import models
from django.utils.translation import gettext_lazy as _


class Languages(models.TextChoices):
    """String based enum for language choice."""

    PYTHON = "Python", _("Python")


class TestResultStatus(models.TextChoices):
    """String based enum for test result status choice."""

    COMPLETE = "Complete", _("Complete")
    FAIL = "Fail", _("Fail")
    ERROR = "Error", _("Error")


class SolutionStatus(models.TextChoices):
    """String based enum for solution status choice."""

    PENDING = "Pending", _("Pending")
    IN_PROGRESS = "In Progress", _("In Progress")
    COMPLETED = "Completed", _("Completed")


class Complexity(models.TextChoices):
    """String based enum for issue complexity choice."""

    EASY = "Easy", _("Easy")
    MEDIUM = "Medium", _("Medium")
    HARD = "Hard", _("Hard")

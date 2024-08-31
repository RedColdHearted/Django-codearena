from apps.issues.models.constants import Complexity


class Scores:
    """Issue type scores."""

    POINTS = {
        Complexity.EASY: 3,
        Complexity.MEDIUM: 5,
        Complexity.HARD: 7,
    }

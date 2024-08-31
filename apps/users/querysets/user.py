from typing import Self

from django.db import models

from .constants import Scores


class UserQuerySet(models.QuerySet):
    """Queryset class for 'User' model."""

    def with_solved_issues(self) -> Self:
        """Annotate user with count of solved issues, scores, and rank.

        This method performs the following operations:
        - Count of solved issues for each users
        - Calculate scores for solved issues: Computes the total score
            for each user by multiplying the count of solved issues by their
            corresponding point values.
        - Order by total_scores

        """
        points = Scores.POINTS
        count_conditions = {
            f"{complexity}_count": models.Count(
                "solved_issues",
                filter=models.Q(solved_issues__issue__complexity=complexity),
            )
            for complexity in points
        }
        return (
            self.prefetch_related(
                "solved_issues",
            )
            .alias(
                **count_conditions,
            )
            .annotate(
                solved_issues_count=models.Count("solved_issues"),
                total_scores=models.ExpressionWrapper(
                    sum(
                        models.F(f"{complexity}_count") * points[complexity]
                        for complexity in points
                    ),
                    output_field=models.IntegerField(),
                ),
            )
            .order_by("-total_scores", "username")
        )

    def users_rank(self) -> Self:
        """Annotates the given queryset with rank."""
        ordered_ids = self.values_list("id", flat=True)
        return self.annotate(
            rank=models.Case(
                *[
                    models.When(pk=pk, then=position)
                    for position, pk in enumerate(
                        ordered_ids,
                        start=1,
                    )
                ],
            ),
        )

from apps.issues.models import SolvedIssue

from ...models import User


def test_user_queryset_with_solved_users(
    multiple_solved_issue_with_users: list[SolvedIssue],
) -> None:
    """Ensure that 'with_solved_users' and 'users_rank' methods work right."""
    queryset = User.objects.with_solved_issues().users_rank()
    expected_data_list = [
        {
            "solved_issues_count": 1,
            "total_scores": 3,
            "rank": 3,
        },
        {
            "solved_issues_count": 1,
            "total_scores": 5,
            "rank": 2,
        },
        {
            "solved_issues_count": 1,
            "total_scores": 7,
            "rank": 1,
        },
    ]

    for issue, expected_data in zip(
        multiple_solved_issue_with_users,
        expected_data_list,
        strict=False,
    ):
        user_data = queryset.get(
            username=issue.user,
        )
        assert (
            user_data.solved_issues_count
            == (expected_data["solved_issues_count"])
        )
        assert user_data.total_scores == expected_data["total_scores"]
        assert user_data.rank == expected_data["rank"]

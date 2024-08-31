from django.urls import reverse_lazy


def get_issue_solve_url(issue_id: int) -> str:
    """Return lazy url to issue-solve."""
    return reverse_lazy(
        "issues:issue-solve",
        args=(issue_id,),
    )


def get_issue_like_url(issue_id: int) -> str:
    """Return lazy url to issue-like."""
    return reverse_lazy(
        "issues:issue-like",
        args=(issue_id,),
    )


def get_test_case_result_api_url(solution_id: int) -> str:
    """Return lazy url to test-case-result-by-solution."""
    return reverse_lazy(
        "v1:test-case-result-by-solution",
        args=(solution_id,),
    )

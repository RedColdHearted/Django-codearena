import http

from rest_framework import test

from ... import factories
from .. import shortcuts


def test_test_case_result_by_solution(
    user_api_client: test.APIClient,
) -> None:
    """Ensure that requests to endpoint return a TestCaseResult instances."""
    solution = factories.SolutionFactory()
    factories.TestCaseResultFactory.create_batch(
        5,
        solution=solution,
    )
    url = shortcuts.get_test_case_result_api_url(solution.id)

    response = user_api_client.get(url)

    assert response.status_code == http.HTTPStatus.OK
    assert response.data["count"] == 5


def test_test_case_result_by_non_existent_solution(
    user_api_client: test.APIClient,
) -> None:
    """Ensure that requests to endpoint return a TestCaseResult instances."""
    url = shortcuts.get_test_case_result_api_url(solution_id=10)

    response = user_api_client.get(url)

    assert response.status_code == http.HTTPStatus.OK
    assert response.data["count"] == 0
    assert not response.data["results"]

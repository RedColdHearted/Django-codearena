import docker
import pytest
from docker.models.containers import Container
from pytest_mock import MockerFixture

from ... import models
from ...services.processing_solutions import constants
from ...services.processing_solutions.docker_runner import (
    build_image,
    exec_test_by_command_line,
    run_container,
    run_solution_with_multiple_test_cases,
    run_solution_with_test_case,
    validate_solution,
)
from ...services.processing_solutions.errors import TestsError
from ...services.processing_solutions.handlers import PythonHandler


def test_build_docker_image_and_run_container(
    docker_client: docker.client.DockerClient,
) -> None:
    """Ensure that image build and container run work with language handler."""
    language_handler = PythonHandler()
    image = build_image(
        client=docker_client,
        docker_file_path=language_handler.docker_file_path,
        image_tag=language_handler.docker_image_name,
    )
    container = run_container(
        client=docker_client,
        docker_image=image,
        docker_container_name=language_handler.docker_container_name,
    )

    assert image
    assert language_handler.docker_image_name in image.tags
    assert container
    assert language_handler.docker_container_name == container.name


def test_exec_test_by_command_line(container_with_python: Container) -> None:
    """Ensure that container `exec_test_by_command_line` logic works."""
    language_handler = PythonHandler()
    language_handler.prepare_file_to_exec(
        "def func(a, b):\n    return a + b",
        "print(func(2, 2))",
    )

    exec_data = exec_test_by_command_line(
        container=container_with_python,
        docker_run_command=language_handler.get_docker_command_line(),
        timeout=100,
    )
    language_handler.cleanup_file_to_exec()

    assert exec_data.execution_log == "4\n"
    assert exec_data.exit_code == 0
    assert exec_data.time_used
    assert exec_data.memory_used


def test_solution_with_test_case(
    container_with_python: Container,
    python_test_case: models.TestCase,
    python_solution_with_user: models.Solution,
    mocker: MockerFixture,
) -> None:
    """Test `run_solution_with_test_case` functionality.

    This test uses to ensure that `run_solution_with_test_case` return
    unsaved in db `TestCaseResult` instance which stores correct information.

    """
    language_handler = PythonHandler()
    instance = run_solution_with_test_case(
        solution=python_solution_with_user,
        test_case=python_test_case,
        container=container_with_python,
        language_handler=language_handler,
    )
    assert isinstance(instance, models.TestCaseResult)
    assert instance._state.adding
    assert instance.solution == python_solution_with_user
    assert instance.test_case == python_test_case
    assert (
        instance.status == models.constants.TestResultStatus.COMPLETE
    ), instance.execution_log
    assert instance.time_used
    assert instance.memory_used


def test_run_solution_with_multiple_test_cases(
    python_solution_with_user: models.Solution,
    multiple_python_test_cases: tuple[models.TestCase],
    mocker: MockerFixture,
) -> None:
    """Test `run_solution_with_multiple_test_cases` functionality."""
    test_case_results = run_solution_with_multiple_test_cases(
        python_solution_with_user,
        multiple_python_test_cases,
    )
    for instance in test_case_results:
        assert isinstance(instance, models.TestCaseResult)
        assert instance._state.adding
        assert instance.solution == python_solution_with_user
        assert instance.test_case in multiple_python_test_cases
        assert (
            instance.status == models.constants.TestResultStatus.COMPLETE
        ), instance.execution_log
        assert instance.time_used
        assert instance.memory_used


@pytest.mark.parametrize(
    "test_cases",
    [
        [],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    ],
)
def test_run_solution_with_multiple_test_cases_by_invalid_test_cases_amount(
    test_cases: list[int],
    solution: models.Solution,
) -> None:
    """Ensure that invalid test case amount raise exception."""
    with pytest.raises(TestsError) as exc_info:
        run_solution_with_multiple_test_cases(solution, test_cases)
    assert constants.TESTS_CASES_ERROR_MESSAGE in str(exc_info.value)


def test_correct_validate_solution(
    python_solution_with_user: models.Solution,
    multiple_python_test_cases: tuple[models.TestCase],
    mocker: MockerFixture,
) -> None:
    """Ensure that correct `validate_solution` functionality works."""
    validate_solution(python_solution_with_user)

    mocker.patch(
        "apps.issues.models.TestCase.objects.order_by",
        return_value=multiple_python_test_cases,
    )

    assert models.TestCaseResult.objects.filter(
        solution=python_solution_with_user,
    ).exists()
    assert python_solution_with_user.testing_status == (
        models.constants.SolutionStatus.COMPLETED
    )
    # Ensure that only COMPLETED solution exists
    assert (
        not models.TestCaseResult.objects.filter(
            solution=python_solution_with_user,
        )
        .exclude(
            status=models.constants.TestResultStatus.COMPLETE,
        )
        .exists()
    )

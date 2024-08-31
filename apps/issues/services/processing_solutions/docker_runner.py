import pathlib
import time
import typing

import docker
import docker.errors
import docker.models
from docker.client import DockerClient
from docker.models.containers import Container
from docker.models.images import Image

from ... import models
from . import constants, dataclasses, errors, handlers


def build_image(
    client: DockerClient,
    docker_file_path: pathlib.Path,
    image_tag: str,
) -> Image:
    """Build docker image and return image instance.

    Implemented by using docs: https://shorturl.at/SxeVa.

    """
    # Try to find needed image
    try:
        return client.images.get(image_tag)
    except docker.errors.ImageNotFound:
        # Otherwise creating new one
        image, _ = client.images.build(
            path=str(docker_file_path),
            tag=image_tag,
        )
        return image


def run_container(
    client: DockerClient,
    docker_image: Image,
    docker_container_name: str,
) -> Container:
    """Run docker container and return container instance.

    Implemented by using docs: https://shorturl.at/TTI91.

    """
    # Try to find needed container
    try:
        container = client.containers.get(docker_container_name)
        if container.status != "running":
            container.start()
        return container
    except docker.errors.NotFound:
        # Otherwise creating new one
        return client.containers.run(
            image=docker_image,
            name=docker_container_name,
            network_disabled=True,
            detach=True,
            mem_limit=constants.DOCKER_MEM_LIMIT,
            cpu_quota=constants.DOCKER_CPU_LIMIT,
            volumes={
                constants.EXECUTION_FILE_DIR.resolve(): {
                    "bind": "/test_runner",
                    "mode": "consistent",
                },
            },
            security_opt=["no-new-privileges"],
        )


def exec_test_by_command_line(
    container: Container,
    docker_run_command: str,
    timeout: int,
) -> dataclasses.ExecData:
    """Run a command that exec test file in docker container.

    Implemented by using docs: https://shorturl.at/qTtcQ.

    """
    start_time = time.perf_counter()
    exec_result = container.exec_run(
        f"timeout {timeout} {docker_run_command}",
    )
    end_time = time.perf_counter()
    memory_used = round(
        container.stats(
            stream=False,
        )["memory_stats"]["usage"]
        / constants.BYTES_IN_MEGABYTE,
        2,
    )
    if (time_used := round(end_time - start_time, 3)) > timeout:
        return dataclasses.ExecData(
            execution_log="Test time is over",
            exit_code=constants.TIMEOUT_CODE,
            time_used=time_used,
            memory_used=memory_used,
        )
    return dataclasses.ExecData(
        execution_log=exec_result.output.decode(),
        exit_code=exec_result.exit_code,
        time_used=time_used,
        memory_used=memory_used,
    )


def run_solution_with_test_case(
    solution: models.Solution,
    test_case: models.TestCase,
    container: Container,
    language_handler: type[handlers.BaseLanguageHandler],
) -> models.TestCaseResult:
    """Run solution with test case and return `TestCaseResult` instance."""
    language_handler.prepare_file_to_exec(
        solution.content,
        test_case.input_data,
    )
    exec_data = exec_test_by_command_line(
        container=container,
        docker_run_command=language_handler.get_docker_command_line(),
        timeout=test_case.allocated_time,
    )
    language_handler.cleanup_file_to_exec()
    status = models.constants.TestResultStatus.COMPLETE
    execution_log = exec_data.execution_log
    excepted_output = test_case.excepted_output.replace("\\n", "\n")

    if excepted_output != execution_log:
        if not exec_data.exit_code:
            execution_log = f"{excepted_output} != {execution_log}"
            status = models.constants.TestResultStatus.FAIL
        else:
            status = models.constants.TestResultStatus.ERROR

    return models.TestCaseResult(
        solution=solution,
        test_case=test_case,
        status=status,
        execution_log=execution_log,
        time_used=exec_data.time_used,
        memory_used=exec_data.memory_used,
    )


def run_solution_with_multiple_test_cases(
    solution: models.Solution,
    test_cases: typing.Iterable[models.TestCase],
) -> list[models.TestCase]:
    """Perform logic of running tests for solution."""
    tests_amount = len(test_cases)
    if not constants.MIN_TEST_CASES < tests_amount <= constants.MAX_TEST_CASES:
        raise errors.TestsError(constants.TESTS_CASES_ERROR_MESSAGE)

    language_handler = handlers.PythonHandler()

    # Preparing docker client, image and container
    client = docker.from_env(environment={})
    docker_image = build_image(
        client=client,
        docker_file_path=language_handler.docker_file_path,
        image_tag=language_handler.docker_image_name,
    )
    container = run_container(
        client=client,
        docker_image=docker_image,
        docker_container_name=language_handler.docker_container_name,
    )
    return [
        run_solution_with_test_case(
            solution=solution,
            test_case=test_case,
            container=container,
            language_handler=language_handler,
        )
        for test_case in test_cases
    ]


def create_solved_issue_or_do_nothing(
    test_case_results: list[models.TestCaseResult],
    solution: models.Solution,
) -> None:
    """Create or not `SolvedIssue` instance."""
    # Checking if all tests are complete and create SolvedIssue instance
    # if the same one doesn't exist
    if (
        all(
            test_cases_result.status
            == models.constants.TestResultStatus.COMPLETE
            for test_cases_result in test_case_results
        )
        and not models.SolvedIssue.objects.filter(
            issue=solution.issue,
            user=solution.user,
        ).exists()
    ):
        solved_issue = models.SolvedIssue(
            issue=solution.issue,
            user=solution.user,
        )
        solved_issue.save()


def validate_solution(solution: models.Solution) -> None:
    """Perform validation of solution by tests in docker."""
    solution.testing_status = models.constants.SolutionStatus.IN_PROGRESS
    solution.save()

    models.TestCaseResult.objects.filter(solution=solution).delete()
    test_case_results = run_solution_with_multiple_test_cases(
        solution=solution,
        test_cases=models.TestCase.objects.filter(
            issue=solution.issue,
            language=solution.language,
        ).order_by("order"),
    )

    models.TestCaseResult.objects.bulk_create(test_case_results)
    solution.testing_status = models.constants.SolutionStatus.COMPLETED
    solution.save()

    create_solved_issue_or_do_nothing(test_case_results, solution)

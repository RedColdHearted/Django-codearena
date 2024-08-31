import typing

import docker
import pytest
import pytest_django
from docker.models.containers import Container
from docker.models.images import Image

from apps.users.models import User

from ... import factories, models
from ...services.processing_solutions.docker_runner import (
    build_image,
    run_container,
)
from ...services.processing_solutions.handlers import PythonHandler

python_handler = PythonHandler()


@pytest.fixture(scope="module")
def docker_client() -> (
    typing.Generator[docker.client.DockerClient, None, None]
):
    """Return docker client."""
    client = docker.from_env()
    yield client
    client.close()


@pytest.fixture(scope="module")
def image_with_python(docker_client: docker.client.DockerClient) -> Image:
    """Return image of docker container for python solutions."""
    return build_image(
        client=docker_client,
        docker_file_path=python_handler.docker_file_path,
        image_tag=python_handler.docker_image_name,
    )


@pytest.fixture(scope="module")
def container_with_python(
    docker_client: docker.client.DockerClient,
    image_with_python: Image,
) -> Container:
    """Return docker container instance for python solutions.

    Restarting container because of consistency issues for tracking changes
    in mounted directories to container, especially in pre-commit hooks.

    """
    container = run_container(
        client=docker_client,
        docker_image=image_with_python,
        docker_container_name=python_handler.docker_container_name,
    )
    container.restart()
    return container


@pytest.fixture
def python_solution_with_user(
    issue: models.Issue,
    user: User,
    django_db_blocker: pytest_django.DjangoDbBlocker,
) -> models.Solution:
    """Return Solution with python instance for tests."""
    with django_db_blocker.unblock():
        return factories.SolutionFactory(
            user=user,
            issue=issue,
            language=models.constants.Languages.PYTHON,
            content="def func(a, b):\n    return a + b",
        )


@pytest.fixture
def python_test_case(
    issue: models.Issue,
    django_db_blocker: pytest_django.DjangoDbBlocker,
) -> models.TestCase:
    """Return `TestCase` python instance for tests."""
    with django_db_blocker.unblock():
        return factories.TestCaseFactory(
            issue=issue,
            input_data="print(func(2, 2))",
            excepted_output="4\n",
            order=1,
            allocated_time=6,
        )


@pytest.fixture
def multiple_python_test_cases(
    issue: models.Issue,
    django_db_blocker: pytest_django.DjangoDbBlocker,
) -> tuple[models.TestCase]:
    """Return multiple `TestCase` python instances for tests."""
    with django_db_blocker.unblock():
        return (
            factories.TestCaseFactory(
                issue=issue,
                input_data="print(func(2, 2))",
                excepted_output="4\n",
                order=1,
                allocated_time=6,
            ),
            factories.TestCaseFactory(
                issue=issue,
                input_data="print(func(0, 0))",
                excepted_output="0\n",
                order=2,
                allocated_time=6,
            ),
        )

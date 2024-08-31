from celery import shared_task

from . import models
from .services.processing_solutions import docker_runner


@shared_task
def run_solution_tests(solution_id: int) -> None:
    """Task to perform test cases run for solution."""
    docker_runner.validate_solution(
        solution=models.Solution.objects.filter(id=solution_id).first(),
    )

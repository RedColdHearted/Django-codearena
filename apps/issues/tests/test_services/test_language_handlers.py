from ...services.processing_solutions.handlers import PythonHandler


def test_get_docker_command_line_from_python() -> None:
    """Ensure that handler's get_docker_command_line works."""
    assert PythonHandler().get_docker_command_line() == "python solution.py"

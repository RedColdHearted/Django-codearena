import pathlib

from .. import constants
from . import BaseLanguageHandler


class PythonHandler(BaseLanguageHandler):
    """Python handler for tests run in docker."""

    docker_image_name = "python_image:latest"
    docker_container_name = "python_container"
    docker_file_path = constants.DOCKERFILE_FOLDER / pathlib.Path("python")
    execution_file = constants.EXECUTION_FILE_DIR / pathlib.Path("solution.py")

    def get_docker_command_line(
        self,
    ) -> str:
        """Return string of python command for exec."""
        return f"python {self.execution_file.name}"

    def prepare_file_to_exec(
        self,
        content: str,
        input_data: str,
    ) -> None:
        """Prepare file which need to exec while tests run."""
        self.execution_file.unlink(missing_ok=True)

        self.execution_file.write_text(
            f"{content}\r\n{input_data}",
        )

    def cleanup_file_to_exec(self) -> None:
        """Cleanup file which need to exec while tests run."""
        self.execution_file.touch(exist_ok=True)

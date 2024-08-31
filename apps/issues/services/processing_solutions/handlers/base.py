import abc
import pathlib


class BaseLanguageHandler(abc.ABC):
    """Base language handler for tests run in docker."""

    docker_image_name: str
    docker_container_name: str
    docker_file_path: pathlib.Path
    execution_file: pathlib.Path

    @abc.abstractmethod
    def get_docker_command_line(self) -> str:
        """Return string of command for exec."""
        raise NotImplementedError

    def prepare_file_to_exec(self, content: str, input_data: str) -> None:
        """Prepare file which need to exec while tests run."""
        raise NotImplementedError

    def cleanup_file_to_exec(self) -> None:
        """Cleanup file which need to exec while tests run."""
        raise NotImplementedError

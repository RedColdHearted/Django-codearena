import pathlib

EXECUTION_FILE_DIR = pathlib.Path(
    "apps/issues/services/processing_solutions/execution_files/",
)
DOCKERFILE_FOLDER = pathlib.Path(
    "apps/issues/services/processing_solutions/docker_config/",
)
DOCKER_MEM_LIMIT = "256m"  # 256 megabytes - Total limit on RAM usage
DOCKER_CPU_LIMIT = 40000  # 40% - Total limit on processor usage
MIN_TEST_CASES = 0
MAX_TEST_CASES = 10
TESTS_CASES_ERROR_MESSAGE = (
    f"Test cases amount should be between {MIN_TEST_CASES}"
    f" and {MAX_TEST_CASES}."
)
TIMEOUT_CODE = 2
LANGUAGE_HANDLER_ERROR_MESSAGE = "'{}' such handler not found"
BYTES_IN_MEGABYTE = 1048576

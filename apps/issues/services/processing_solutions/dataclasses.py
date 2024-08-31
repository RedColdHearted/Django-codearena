from dataclasses import dataclass

from ... import models


@dataclass(frozen=True)
class ExecData:
    """Dataclass of result test exec in docker."""

    execution_log: str
    exit_code: int
    time_used: float
    memory_used: float


@dataclass(frozen=True)
class TestsRunData:
    """Dataclass that represent data of results for all solution's tests."""

    test_case_results: list[models.TestCaseResult]
    average_time_usage: float
    average_memory_usage: float

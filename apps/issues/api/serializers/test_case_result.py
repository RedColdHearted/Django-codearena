from apps.core.api.serializers import ModelBaseSerializer

from ...models import TestCaseResult


class TestCaseResultModelSerializer(ModelBaseSerializer):
    """Model serializer for `TestCaseResult` model."""

    class Meta:
        model = TestCaseResult
        fields = (
            "solution",
            "test_case",
            "status",
            "execution_log",
            "time_used",
            "memory_used",
            "modified",
            "created",
            "id",
        )

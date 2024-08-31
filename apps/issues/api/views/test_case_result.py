from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from ... import models
from .. import serializers


class TestCaseResultViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet for `TestCaseResult` model."""

    serializer_class = serializers.TestCaseResultModelSerializer
    permission_classes = (IsAuthenticated,)
    search_fields = (
        "status",
    )
    ordering_fields = (
        "solution",
        "status",
        "modified",
        "created",
        "id",
    )
    queryset = models.TestCaseResult.objects.all()

    def get_queryset(self):
        """Return queryset of TestCaseResult instances."""
        queryset = super().get_queryset()
        solution_id = self.kwargs.get("solution_id")
        if solution_id is not None:
            queryset = queryset.filter(solution__id=solution_id)
        return queryset

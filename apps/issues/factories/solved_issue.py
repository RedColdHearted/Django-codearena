import factory

from ..models import SolvedIssue
from .issue import IssueFactory


class SolvedIssueFactory(factory.django.DjangoModelFactory):
    """Factory to generate test SolvedIssue instance."""

    user = factory.SubFactory("apps.users.factories.UserFactory")
    issue = factory.SubFactory(IssueFactory)

    class Meta:
        model = SolvedIssue

import factory

from .. import models
from ..factories.issue import IssueFactory


class ExampleFactory(factory.django.DjangoModelFactory):
    """Factory to generate test Example instance."""

    issue = factory.SubFactory(IssueFactory)
    input = factory.Faker("paragraph")
    output = factory.Faker("paragraph")
    explanation = factory.Faker("paragraph")
    order = factory.Faker(
        "pyint",
        min_value=1,
        max_value=10,
    )

    class Meta:
        model = models.Example
        django_get_or_create = (
            "order",
            "issue",
        )

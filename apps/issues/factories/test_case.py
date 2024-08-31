import factory
import factory.fuzzy

from .. import factories, models


class TestCaseFactory(factory.django.DjangoModelFactory):
    """Factory to generate test TestCase instance."""

    issue = factory.SubFactory(factories.IssueFactory)
    language = factory.fuzzy.FuzzyChoice(models.constants.Languages.values)
    input_data = factory.Faker("paragraph")
    excepted_output = factory.Faker("paragraph")
    order = factory.Faker(
        "pyint",
        min_value=1,
        max_value=10,
    )
    allocated_time = factory.Faker(
        "pyint",
        min_value=3,
        max_value=6,
    )
    allocated_memory = factory.Faker(
        "pyint",
        min_value=8,
        max_value=256,
    )

    class Meta:
        model = models.TestCase
        django_get_or_create = (
            "order",
            "issue",
        )

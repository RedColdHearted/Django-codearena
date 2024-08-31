import factory
import factory.fuzzy

from .. import factories, models


class TestCaseResultFactory(factory.django.DjangoModelFactory):
    """Factory to generate test TestCaseResult instance."""

    test_case = factory.SubFactory(factories.TestCaseFactory)
    status = factory.fuzzy.FuzzyChoice(
        models.constants.TestResultStatus.values,
    )
    execution_log = factory.Faker("paragraph")
    time_used = factory.Faker(
        "pyfloat",
        left_digits=1,
        right_digits=3,
        min_value=1,
        max_value=6,
    )
    memory_used = factory.Faker(
        "pyfloat",
        left_digits=3,
        right_digits=1,
        min_value=1,
        max_value=6,
    )

    class Meta:
        model = models.TestCaseResult

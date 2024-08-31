import factory
import factory.fuzzy

from apps.users.factories import UserFactory

from .. import factories, models


class SolutionFactory(factory.django.DjangoModelFactory):
    """Factory to generate test Solution instance."""

    user = factory.SubFactory(UserFactory)
    issue = factory.SubFactory(factories.IssueFactory)
    language = factory.fuzzy.FuzzyChoice(models.constants.Languages.values)
    content = factory.Faker("paragraph")
    average_time_usage = factory.Faker(
        "pyfloat",
        left_digits=1,
        right_digits=10,
        min_value=1,
        max_value=6,
    )
    average_memory_usage = factory.Faker(
        "pyfloat",
        left_digits=3,
        right_digits=10,
        min_value=1,
        max_value=256,
    )
    testing_status = factory.fuzzy.FuzzyChoice(
        models.constants.SolutionStatus.values,
    )

    class Meta:
        model = models.Solution

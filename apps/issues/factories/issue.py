import factory
import factory.fuzzy

from .. import models


class IssueFactory(factory.django.DjangoModelFactory):
    """Factory to generate test Issue instance."""

    title = factory.Faker("word")
    description = factory.Faker("paragraph")
    hint = factory.Faker("paragraph")
    complexity = factory.fuzzy.FuzzyChoice(models.constants.Complexity.values)

    class Meta:
        model = models.Issue

    @factory.post_generation
    def tags(
        self,
        create: bool,
        extracted: None | list[int],
        **kwargs,
    ) -> None:
        """Add a Tag instance for many to many field."""
        if not create or not extracted:
            return
        self.tags.set(extracted)

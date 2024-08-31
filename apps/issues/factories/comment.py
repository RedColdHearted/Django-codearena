import factory

from apps.users.factories import UserFactory

from .. import models


class IssueCommentFactory(factory.django.DjangoModelFactory):
    """Factory to generate test Comment instance."""

    user = factory.SubFactory(UserFactory)
    content = factory.Faker("paragraph")

    content_object = factory.SubFactory(
        "apps.issues.factories.IssueFactory",
    )

    class Meta:
        model = models.Comment

    @factory.post_generation
    def likes(
        self,
        create: bool,
        extracted: None | list[int],
        **kwargs,
    ) -> None:
        """Add a User instance for many to many field."""
        if not create or not extracted:
            return
        self.likes.set(extracted)

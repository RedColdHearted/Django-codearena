import factory

from .. import models


class TagFactory(factory.django.DjangoModelFactory):
    """Factory to generate test Tag instance."""

    title = factory.Faker("word")

    class Meta:
        model = models.Tag
        django_get_or_create = ("title",)

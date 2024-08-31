import factory

from ..models import Achievement


class AchievementFactory(factory.django.DjangoModelFactory):
    """Factory to generate test Achievement instance."""

    title = factory.Faker("word")
    description = factory.Faker("sentence")
    image = factory.django.ImageField(color="magenta")

    class Meta:
        model = Achievement

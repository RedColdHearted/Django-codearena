import uuid

from django.conf import settings

import factory

from ..models import User

DEFAULT_PASSWORD = "Test111!"  # noqa: S105


class UserFactory(factory.django.DjangoModelFactory):
    """Factory to generate test User instance."""

    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    avatar = factory.django.ImageField(color="magenta")
    password = factory.django.Password(password=DEFAULT_PASSWORD)

    class Meta:
        model = User

    @factory.lazy_attribute
    def email(self) -> str:
        """Return formatted email."""
        return (
            f"{uuid.uuid4()}@"
            f"{settings.APP_LABEL.lower().replace(' ', '-')}.com"
        )

    @factory.post_generation
    def achievements(
        self,
        create: bool,
        extracted: None | list[int],
        **kwargs,
    ) -> None:
        """Add achievements to the user after creation."""
        if not create or not extracted:
            return

        self.achievements.set(extracted)


class AdminUserFactory(UserFactory):
    """Factory to generate test User model with admin privileges."""

    is_superuser = True
    is_staff = True

    class Meta:
        model = User

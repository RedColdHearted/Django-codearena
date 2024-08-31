from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Comment(BaseModel):
    """Represent codearena's comment in db."""

    user = models.ForeignKey(
        to="users.User",
        verbose_name=_("User id"),
        on_delete=models.CASCADE,
        related_name="comments",
    )
    content = models.TextField(
        verbose_name=_("Content"),
    )
    likes = models.ManyToManyField(
        to="users.User",
        verbose_name=_("Comment likes"),
        help_text=_("User's likes to comment"),
        related_name="comments_likes",
        blank=True,
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField(
        verbose_name=_("Object ID"),
    )
    content_object = GenericForeignKey(
        "content_type",
        "object_id",
    )

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comment")

    def __str__(self) -> str:
        return f"Comment(User={self.user.id}, object_id={self.object_id})"

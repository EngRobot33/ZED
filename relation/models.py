import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.models import BaseModel

User = get_user_model()


class Relation(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    following = models.ForeignKey(
        User,
        verbose_name=_('following'),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='following'
    )
    follower = models.ForeignKey(
        User,
        verbose_name=_('follower'),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='follower'
    )

    class Meta:
        verbose_name = _("Relation")
        verbose_name_plural = _("Relations")
        db_table = "Relation"

    def __str__(self):
        return f'{self.follower} -> {self.following}'

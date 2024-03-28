from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.models import BaseModel

User = get_user_model()


class Relation(BaseModel):
    following = models.ForeignKey(
        User,
        verbose_name=_('following'),
        on_delete=models.CASCADE,
        related_name='followers',
        blank=True,
        null=True,
    )
    follower = models.ForeignKey(
        User,
        verbose_name=_('follower'),
        on_delete=models.CASCADE,
        related_name='following_users',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Relation")
        verbose_name_plural = _("Relations")
        db_table = "relation"

    def __str__(self):
        return f'{self.follower} -> {self.following}'

    def clean(self):
        if self.following == self.follower:
            raise ValidationError("A user cannot follow themselves.")
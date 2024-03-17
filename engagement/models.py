import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from content.models import Post, Comment
from utils.models import BaseModel

User = get_user_model()


class LikedPost(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    like_count = models.IntegerField(verbose_name=_('post like count'), default=0)
    post = models.ForeignKey(
        Post,
        verbose_name=_('liked post'),
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    liker = models.ForeignKey(
        User,
        verbose_name=_('post liker'),
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _("LikedPost")
        verbose_name_plural = _("LikedPosts")
        db_table = "LikedPost"

    def __str__(self):
        return f'{self.liker} -> {self.post}'


class LikedComment(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    like_count = models.IntegerField(verbose_name=_('comment like count'), default=0)
    comment = models.ForeignKey(
        Comment,
        verbose_name=_('liked comment'),
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    liker = models.ForeignKey(
        User,
        verbose_name=_('comment liker'),
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _("LikedComment")
        verbose_name_plural = _("LikedComments")
        db_table = "LikedComment"

    def __str__(self):
        return f'{self.liker} -> {self.comment}'


class LikeNotification(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notified = models.ForeignKey(
        User,
        verbose_name=_('notified user'),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='notified'
    )
    notifier = models.ForeignKey(
        User,
        verbose_name=_('notifier user'),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='notifier'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _("LikeNotification")
        verbose_name_plural = _("LikeNotifications")
        db_table = "LikeNotification"

    def __str__(self):
        return f'{self.notifier} -> {self.notified}'

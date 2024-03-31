import re

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.models import BaseModel

User = get_user_model()


class Topic(BaseModel):
    name = models.CharField(max_length=32, verbose_name=_('topic name'))

    class Meta:
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")
        db_table = "topic"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = str(self.name).lower().replace(' ', '-')
        super().save(*args, **kwargs)

class AbstractPost(BaseModel):
    content = models.TextField(verbose_name=_('content'))
    image = models.ImageField(verbose_name=_('image'), upload_to="post_photos/", blank=True, null=True)
    like_count = models.IntegerField(verbose_name=_('like count'), default=0)
    comment_count = models.IntegerField(verbose_name=_('comment count'), default=0)
    author = models.ForeignKey(
        User,
        verbose_name=_('author'),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='%(class)ss',
        related_query_name='%(class)s'
    )
    topic = models.ManyToManyField(
        Topic,
        verbose_name=_('post topic'),
        blank=True,
        related_name='%(class)ss',
        related_query_name='%(class)s'
    )

    def __str__(self):
        content = str(self.content).split()[:5]
        content = ' '.join(content)
        return f'{self.author} | {content}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        hashtags = re.findall(r'#\w+', str(self.content))

        for hashtag in hashtags:
            topic_queryset = Topic.objects.filter(name__iexact=hashtag)

            if topic_queryset.exists():
                self.topic.add(*topic_queryset)
            else:
                new_topic = Topic.objects.create(name=hashtag)
                self.topic.add(new_topic)    
    class Meta:
        abstract = True

class Post(AbstractPost):
    is_repost = models.BooleanField(default=False)
    original_post = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name="quotes",
        on_delete=models.CASCADE
    )
    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        db_table = "post"

class Comment(AbstractPost):
    post = models.ForeignKey(
        Post,
        verbose_name=_('post'),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='comments',
    )
    parent_comment = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name="child_comments",
        on_delete=models.CASCADE
    )
    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        db_table = "comment"

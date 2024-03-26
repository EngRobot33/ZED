from django.contrib import admin

from .models import Topic, Post, Comment, Repost

admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Repost)

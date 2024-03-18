from django.contrib import admin
from .models import LikedPost, LikedComment, LikeNotification

admin.site.register(LikedPost)
admin.site.register(LikedComment)
admin.site.register(LikeNotification)

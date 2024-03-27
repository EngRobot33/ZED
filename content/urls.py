from django.urls import path

from .views import *

app_name = 'content'

urlpatterns = [
    path('', index, name='index'),
    path('home/<int:page>/', home, name='home'),
    path('post/<uuid:post_id>/', single_post, name='single_post'),
    path('explore/', explore, name='explore'),
    path('explore/<str:topic>/<int:page>/', topic_explore, name='topic_explore'),
    path('profile/', profile, name='profile'),
    path('profile/<str:other_user_username>/', other_user_profile, name='other_user_profile'),
    path('settings/', settings, name='settings'),
    path('search/<str:query>/', search, name='search'),
    path("unfollow/<str:followed_user_username>/", ActionUnFollowView.as_view(), name="actionunfollow"),
]

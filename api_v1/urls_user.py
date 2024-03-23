from django.urls import path
from .views import user_profile, user_posts, user_followerlist, user_followinglist, user_suggestions

urlpatterns = [
 # user enpoints

    # User profile
    #
    # POST /api/v1/user/profile
    #
    # headers: {
    #     Authorization Bearer <access token>
    # }
    # response: {
    #     "username": "zed",
    #     "email": "email",
    #     "first_name": "first_name",
    #     "last_name": "last_name",
    #     "profile_photo": "profile_photo",
    #     "banner_photo": "banner_photo",
    #     "bio": "bio",
    #     "follower_count": 0,
    #     "following_count": 0
    # }
    path('profile',user_profile, name='user_profile'),

    # User posts
    #
    # POST /api/v1/user/posts
    #
    # headers: {
    #     Authorization Bearer <access token>
    # }
    # response: {
    #    count: 1,
    #    next: null,
    #    previous: null,
    #    results: [   
    #     {
    #         "id": 1,
    #         "content": "content",
    #         "image": "image",
    #         "created_at": "created_at",
    #         "updated_at": "updated_at",
    #     }
    #    ]
    # }
    path('posts',user_posts, name='user_posts'),

    # User followers list
    path('followerlist',user_followerlist, name='user_followlist'),

    # User following list
    path('followinglist',user_followinglist, name='user_followlist'),

    # User topic and follow suggestions
    path('suggestions',user_suggestions, name='user_suggestions'),


 
]
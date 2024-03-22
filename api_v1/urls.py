from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import index

urlpatterns = [

    # index
    path('', index, name='index'),
    
    # Get Access Token and Refresh Token
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

    # user endpoints
    path('user/', include('api_v1.urls_user')),

    # post endpoints

    # comment endpoints

    # like endpoints

    # follow endpoints

    # search endpoints

    # notification endpoints

    




]
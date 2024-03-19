from django.urls import path

from .views import *


app_name = 'engagement'

urlpatterns = [
    path('notification/', notification, name='notification'),
]

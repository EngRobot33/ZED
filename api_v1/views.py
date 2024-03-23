from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .serializers import UserSerialized, PostSerialized, FollowerListSerialized, FollowingListSerialized, TopicSerialized
from relation.models import Relation
from utils.base_utils import get_random_topics
from user.models import User



# Create your views here.
def index(request):
    return JsonResponse({'message': 'ZED API v1'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    
    user = request.user
    user = UserSerialized(user)
    return JsonResponse(user.data, safe=False)

    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_posts(request):
    
    user = request.user
    posts = user.posts.all().order_by('-created_time')

    paginator = PageNumberPagination()
    paginator.page_size = 10
    paginated_posts = paginator.paginate_queryset(posts, request)
    result  = PostSerialized(paginated_posts, many=True)
    return paginator.get_paginated_response(result.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_followerlist(request):
    
    user = request.user
    
    followers = Relation.objects.filter(following=user)
    
    followers = FollowerListSerialized(followers, many=True)
    
    return JsonResponse(followers.data, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_followinglist(request):
    
    user = request.user
    
    following = Relation.objects.filter(follower=user)
    
    following = FollowingListSerialized(following, many=True)
    
    return JsonResponse(following.data, safe=False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_suggestions(request):
    
    current_user = request.user

    topics = get_random_topics()

    following_users = Relation.objects.filter(follower__id=current_user.id).values_list('following__id', flat=True)
    random_suggestions = User.objects.exclude(id__in=following_users).exclude(id=current_user.id).order_by('?')[:5]

    serializedTopics = TopicSerialized(topics, many=True)
    suggestions = UserSerialized(random_suggestions, many=True)

    return JsonResponse({'topics': serializedTopics.data, 'suggests': suggestions.data}, safe=False)

    
    

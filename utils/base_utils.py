from django.contrib.auth import get_user_model

from content.models import Post, Topic
from relation.models import Relation

User = get_user_model()


def left_nav_post_form_processing(request, current_user):
    if request.POST.get('hidden_panel_post_submit_btn'):
        post_content = request.POST.get('post_content')
        post_image = request.FILES.get('post_image')

        Post.objects.create(
            author=current_user,
            content=post_content,
            image=post_image
        )


def mobile_post_form_processing(request, current_user):
    if request.POST.get('mobile_hidden_tweet_submit_btn'):
        post_content = request.POST.get('post_content')
        post_image = request.FILES.get('post_image')

        Post.objects.create(
            author=current_user,
            content=post_content,
            image=post_image
        )


def get_random_topics():
    all_topics = Topic.objects.all()
    if all_topics.exists():
        random_topics = all_topics.order_by('?')[:5]
    else:
        random_topics = []

    return random_topics


def get_random_follow_suggestions(current_user):
    following_users = Relation.objects.filter(follower__id=current_user.id).values_list('following__id', flat=True)
    random_suggestions = User.objects.exclude(id__in=following_users).exclude(id=current_user.id).order_by('?')[:5]
    print(random_suggestions)
    return list(random_suggestions)

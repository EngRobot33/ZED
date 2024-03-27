from django.contrib.auth import get_user_model

from content.models import Post, Topic
from engagement.models import LikedPost, LikeNotification, LikedComment
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
    if request.POST.get('mobile_hidden_post_submit_btn'):
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
    return list(random_suggestions)


def toggle_like_post(current_user, current_post):
    if LikedPost.objects.filter(post=current_post, liker=current_user).exists():
        LikedPost.objects.filter(post=current_post, liker=current_user).delete()
        current_post.like_count -= 1
    else:
        LikedPost.objects.create(
            post=current_post,
            liker=current_user
        )
        LikeNotification.objects.create(
            notified=current_post.author,
            notifier=current_user,
            post=current_post,
        )
        current_post.like_count += 1
    current_post.save()


def toggle_like_comment(current_user, current_comment):
    if LikedComment.objects.filter(comment=current_comment, liker=current_user).exists():
        LikedComment.objects.filter(comment=current_comment, liker=current_user).delete()
        current_comment.like_count -= 1
    else:
        LikedComment.objects.create(
            comment=current_comment,
            liker=current_user
        )
        current_comment.like_count += 1
    current_comment.save()


def format_date(date):
    return date.strftime('%b %Y')

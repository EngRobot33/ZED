from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from content.models import Post, Comment
from engagement.models import LikedPost, LikeNotification
from relation.models import Relation
from utils.base_utils import left_nav_post_form_processing, mobile_post_form_processing, get_random_topics, \
    get_random_follow_suggestions
from utils.session_utils import get_current_user

User = get_user_model()


def index(request):
    current_user = get_current_user(request)

    if current_user is None:
        return HttpResponseRedirect('/auth/signup/')
    else:
        return HttpResponseRedirect('/home/0/')


def home(request, page):
    current_user = get_current_user(request)

    if current_user is None:
        return HttpResponseRedirect('/auth/signup/')

    left_nav_post_form_processing(request, current_user)
    mobile_post_form_processing(request, current_user)

    random_topics = get_random_topics()

    if request.POST.get('right_nav_search_submit_btn'):
        search_input = request.POST.get('search_input')
        return HttpResponseRedirect('/search/' + str(search_input) + '/')

    random_follow_suggestions = get_random_follow_suggestions(current_user)

    if request.POST.get('base_random_follow_suggestions_submit_btn'):
        hidden_user_id = request.POST.get('hidden_user_id')
        followed_user = User.objects.get(id=hidden_user_id)

        followings = Relation.objects.filter(follower=current_user)

        for following in followings:
            if following.following == followed_user:
                pass
            else:
                Relation.objects.create(
                    following=followed_user,
                    follower=current_user,
                )

        return HttpResponseRedirect(
            '/profile/' + followed_user.username + '/'
        )

    if request.POST.get('home_page_post_form_submit_btn'):
        post_content = request.POST.get('post_content')
        post_image = request.FILES.get('post_image')

        Post.objects.create(
            author=current_user,
            content=post_content,
            image=post_image
        )

        return HttpResponseRedirect('/')

    followings = Relation.objects.filter(follower=current_user)
    if not followings.exists():
        followings = None

    current_page = page
    next_page = page + 1
    previous_page = page - 1

    post_records_starting_point = current_page * 46
    post_records_ending_point = post_records_starting_point + 46

    post_feed = []

    posts = Post.objects.all().order_by("-id")

    if followings is not None:
        for post in posts:
            for following in followings:
                if post.author == following.following:
                    post_feed.append(post)

    post_feed = post_feed[post_records_starting_point:post_records_ending_point]

    post_comment_amounts = {}
    post_like_amounts = {}
    for post in post_feed:
        post_comments_count = Comment.objects.filter(post=post).count()
        post_comment_amounts[post.id] = post_comments_count

        post_likes_count = LikedPost.objects.filter(post=post).count()
        post_like_amounts[post.id] = post_likes_count

    if request.POST.get('post_cell_comment_submit_btn'):
        current_post_id = request.POST.get('hidden_post_id')
        current_post = Post.objects.get(id=current_post_id)
        return HttpResponseRedirect('/post/' + str(current_post.id) + '/')

    if request.POST.get('post_cell_like_submit_btn'):
        current_post_id = request.POST.get('hidden_post_id')
        current_post = Post.objects.get(id=current_post_id)
        LikedPost.objects.create(
            post=current_post,
            liker=current_user
        )
        LikeNotification.objects.create(
            notified=current_post.author,
            notifier=current_user,
            post=current_post,
        )
        return HttpResponseRedirect('/post/' + str(current_post.id) + '/')

    data = {
        'current_basic_user': current_user,
        'random_follow_suggestions': random_follow_suggestions,
        'random_topics': random_topics,
        'post_feed': post_feed,
        'post_comment_amounts': post_comment_amounts,
        'post_like_amounts': post_like_amounts,
        'current_page': current_page,
        'previous_page': previous_page,
        'next_page': next_page,
    }

    return render(request, 'home/home.html', data)


def single_post(request, post_id):
    current_user = get_current_user(request)

    if current_user is None:
        return HttpResponseRedirect('/auth/signup/')

    random_topics = get_random_topics()

    random_follow_suggestions = get_random_follow_suggestions(current_user)

    current_post = get_object_or_404(Post, id=post_id)

    current_post_likes = LikedPost.objects.filter(post=current_post)

    current_post_comments = Comment.objects.filter(tweet=current_post).order_by('-id')

    if request.POST.get('single_post_like_submit_btn'):
        current_post.like_count += 1
        current_post.save()
        LikeNotification.objects.create(
            notified=current_post.author,
            notifier=current_user,
            post=current_post,
        )
        return HttpResponseRedirect('/post/' + str(current_post.id) + '/')

    if request.POST.get('single_post_reply_submit_btn'):
        reply_content = request.POST.get('reply_content')
        if bool(reply_content) is False or reply_content == "":
            pass
        else:
            Comment.objects.create(
                post=current_post,
                content=reply_content,
                commenter=current_user,
            )
            current_post.comment_count += 1
            current_post.save()
            return HttpResponseRedirect('/post/' + str(current_post.id) + '/')

    if request.POST.get('single_post_comment_like_submit_btn'):
        comment_id = request.POST.get('comment_id')
        comment = Comment.objects.get(id=comment_id)
        comment.like_count += 1
        comment.save()
        return HttpResponseRedirect('/post/' + str(current_post.id) + '/')

    data = {
        'current_user': current_user,
        'random_follow_suggestions': random_follow_suggestions,
        'random_topics': random_topics,
        'current_post': current_post,
        'current_post_likes': current_post_likes,
        'current_post_likes_count': len(current_post_likes),
        'current_post_comments': current_post_comments,
    }

    return render(request, 'home/single_post.html', data)


def explore(request):
    ...


def profile(request):
    ...


def other_user_profile(request, other_user_username):
    ...


def settings(request):
    ...


def search(request, query):
    ...


def topic_explore(request, topic, page):
    ...

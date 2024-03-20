from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render

from engagement.models import LikeNotification
from utils.base_utils import left_nav_post_form_processing, mobile_post_form_processing, get_random_topics, \
    get_random_follow_suggestions
from utils.session_utils import get_current_user


def notification(request):
    current_user = get_current_user(request)

    if current_user is None:
        return HttpResponseRedirect('/auth/signup/')

    left_nav_post_form_processing(request, current_user)
    mobile_post_form_processing(request, current_user)

    random_topics = get_random_topics()
    random_follow_suggestions = get_random_follow_suggestions(current_user)

    try:
        notifications = LikeNotification.objects.filter(notified=current_user).order_by('-created_time')
    except ObjectDoesNotExist:
        notifications = None

    data = {
        'current_user': current_user,
        'random_follow_suggestions': random_follow_suggestions,
        'random_topics': random_topics,
        'notifications': notifications,
    }

    return render(request, 'notifications/notification.html', data)

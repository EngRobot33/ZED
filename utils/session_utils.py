from django.contrib.auth import get_user_model

User = get_user_model()


def get_current_user(request):
    if request.user.is_authenticated:
        return request.user
    else:
        return None

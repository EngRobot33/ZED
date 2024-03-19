from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()


def get_current_user(request):
    current_user = None
    current_user_username = request.session.get('user_username')

    if current_user_username:
        try:
            current_user = User.objects.get(username=current_user_username)
        except User.DoesNotExist:
            pass

    return current_user

"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE","config.settings")
django.setup()

from channels.routing import ProtocolTypeRouter,URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from chat.router import chat_websocket_urlpatterns

from chat.middlewares import TokenAuthenticationMiddleWare

django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter({
    "http" : django_asgi_app,
    "websocket" : AllowedHostsOriginValidator([
        TokenAuthenticationMiddleWare(
            URLRouter(chat_websocket_urlpatterns)
        )
    ])
})
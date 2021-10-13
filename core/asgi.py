"""
ASGI config for simple_django_chat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

django_asgi_application = get_asgi_application()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import chat.routing
from core.utils import TokenAuthMiddlewareStack

application = ProtocolTypeRouter({
  "http": AsgiHandler(),
    "websocket": TokenAuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})

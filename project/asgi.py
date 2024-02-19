"""
ASGI config for project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application


from main.consumers import NotificationConsumer


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')


from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import main.routing
# application = get_asgi_application()
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    "http": django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(
            main.routing.ws_patterns
        )
    ),
})
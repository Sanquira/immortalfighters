"""
ASGI config for immortalfighters project.

It exposes the ASGI callable as a module-level variable named ``application``.
"""

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import chat.routing

# pylint: disable=invalid-name
application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})

"""
Websocket routing patterns for chat application
"""
from django.urls import re_path

from . import consumers

# pylint: disable=invalid-name
websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
]

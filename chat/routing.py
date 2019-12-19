"""
Websocket routing patterns for chat application
"""
from django.conf.urls import url

from . import consumers

# pylint: disable=invalid-name
websocket_urlpatterns = [
    url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
]

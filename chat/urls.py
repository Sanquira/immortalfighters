"""
URL patterns for the chat application
"""

from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.list_rooms, name='list_rooms'),
    url(r'^(?P<room_name>[^/]+)/$', views.single_room, name='single_room'),
]

"""
Views for the chat application
"""
import json
from django.contrib.auth.decorators import login_required
from django.http import Http404

from django.shortcuts import render
from django.utils.safestring import mark_safe

from base.models.ifuser import IFUser
from chat.models import Room


@login_required
def list_rooms(request):
    """List of all rooms"""
    rooms = Room.objects.all()
    user = request.user
    room_list = []
    for room in rooms:
        if check_permission(room, user):
            room_list.append(room)
    return render(request, 'chat/index.html', {"rooms": room_list})


# pylint: disable=unused-argument,fixme
# TODO: Implement permissions for chat
def check_permission(room: Room, user: IFUser) -> bool:
    """Checks if user has permission for said room"""
    return True


@login_required
def single_room(request, room_name):
    """Single room view"""
    room = Room.objects.get(name=room_name)
    if room is None:
        raise Http404('Room %s not found' % room_name)

    user = request.user

    if not check_permission(room, user):
        raise Http404('Room %s not found' % room_name)

    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'room_name': room_name
    })

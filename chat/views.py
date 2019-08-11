from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
import json
# Create your views here.
from django.shortcuts import render
from django.utils.safestring import mark_safe

from chat.models import Room


@login_required
def index(request):
    rooms = Room.objects.all()
    user = request.user
    room_list = []
    for room in rooms:
        if check_permission(room, user):
            room_list.append(room)
    return render(request, 'chat/index.html', {"rooms": room_list})


def check_permission(room, user):
    return True


@login_required
def room(request, room_name):
    rooms = Room.objects.filter(name=room_name)
    if len(rooms) == 0:
        raise Http404('Room %s not found' % room_name)

    room = rooms[0]
    user = request.user

    if not check_permission(room, user):
        raise Http404('Room %s not found' % room_name)

    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'room_name': room_name
    })
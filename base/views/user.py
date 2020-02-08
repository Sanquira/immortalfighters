"""Module for IFUser view."""
import re

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest

COLOR_PATTERN = re.compile("^#(?:[0-9a-fA-F]{3}){1,2}$")


@login_required
def change_user_color(request):
    """
    View for user chat color change.

    Check if request contains newColor field.
    Check if color value is valid.
    Returns color and name of current user or BadRequest.
    """
    if request.POST and 'newColor' in request.POST:
        color = request.POST['newColor']
        if not color.startswith('#'):
            color = '#' + color
        if COLOR_PATTERN.match(color):
            request.user.chat_color = color
            request.user.save()
        return JsonResponse({'user': request.user.username, 'newColor': request.user.chat_color})
    return HttpResponseBadRequest()


@login_required
def change_sound_setting(request):
    """
    View for user chat sound POST

    Return name of current user and sound value or BadRequest
    """
    if request.POST and "newSound" in request.POST:
        request.user.chat_sounds = request.POST['newSound'] == 'true'
        request.user.save()
        return JsonResponse({'user': request.user.username, 'newSound': request.user.chat_sounds})
    return HttpResponseBadRequest()

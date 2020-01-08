"""Module for Base views."""
import re

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeDoneView
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect

from base.forms.auth_form import IFUserCreationForm
from base.models.character import Character
from base.models.ifuser import IFUser
from base.models.profession import BaseProfession
from base.models.race import Race

COLOR_PATTERN = re.compile("^#(?:[0-9a-fA-F]{3}){1,2}$")


def index(request):
    """Renders index page."""
    return render(request, 'base.html')


def banners(request):
    """Renders banners page."""
    return render(request, 'base.html')


def site_rules(request):
    """Renders site rules page."""
    return render(request, 'pages/site_rules.html')


def statistics(request):
    """
    View for statistics.
    
    Data:
    Number of individual race members.
    Number of individual proffesion members.
    Number of registered users.
    Number of online users.
    """
    stats = {
        'races': list(),
        'professions': list(),
        'registered': IFUser.objects.count(),
        'online': IFUser.objects.filter(is_active=True).count()
    }

    for race in Race.objects.all():
        stats['races'].append((race.name, Character.objects.filter(race=race).count()))
    for profession in BaseProfession.objects.filter(parentProf=None):
        stats['professions'].append((profession.name, Character.objects.filter(profession=profession).count()))

    return render(request, 'pages/statistics.html', {'statistics': stats})


def registration(request):
    """View for registration."""
    if request.POST:
        form = IFUserCreationForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            if settings.DEBUG:
                user.is_staff = True
                user.is_superuser = True
            login(request, user)
            
            return redirect('base:index')
    else:
        form = IFUserCreationForm()
    return render(request, 'registration/registration.html', {'form': form})


class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    """
    Class based view for password change.
    
    Inherits from PasswordChangeDoneView.
    Change behavior of default view from rendering template into showing message and redirect to index.
    """
    
    def get(self, request, *args, **kwargs):
        messages.success(request, "Heslo úspěšně změněno.")
        return redirect('base:index')


@login_required
def user_change_color(request):
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

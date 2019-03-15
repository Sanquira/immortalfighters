from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect

from base.forms import RegistrationForm
from base.models import IFUser
from base.models.profession import Profession
from base.models.race import Race


def index(request):
    if request.user.is_authenticated:
        return render(request, 'logged_base.html', {'menu_attrs': MenuWrapper()})
    else:
        return render(request, 'base.html', {'menu_attrs': MenuWrapper()})


def banners(request):
    return render(request, 'base.html')


def log_in(request):
    if request.user.is_anonymous:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
    return redirect('base:index')


def log_out(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('base:index')


def registration(request):
    if request.user.is_anonymous:
        form = RegistrationForm(request.POST or None)
        if request.POST and form.is_valid():
            user = IFUser(email=form.cleaned_data['email'],
                          username=form.cleaned_data['nickname'])
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)

            return redirect('base:index')
        return render(request, 'registration.html', {'menu_attrs': MenuWrapper(), 'form': form})
    else:
        return redirect('base:index')


def site_rules(request):
    return render(request, 'site_rules.html', {'menu_attrs': MenuWrapper()})


class MenuWrapper:
    statistics = {
        'race': list(),
        'profession': list(),
        'registered': 0,
        'online': 0,
        'last_day': 0,
    }

    def __init__(self):
        self.statistics['race'].clear()
        self.statistics['profession'].clear()
        for race in Race:
            self.statistics['race'].append((race.value, 10))
        for profession in Profession:
            self.statistics['profession'].append((profession.value, 10))
        pass

    pass

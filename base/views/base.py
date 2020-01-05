from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from base.forms import RegistrationForm
from base.models import *
from base.models.character import Character
from base.models.profession import BaseProfession
from base.models.race import Race


def index(request):
    return render(request, 'base.html')


def banners(request):
    return render(request, 'base.html')


def log_in(request):
    next_page = None
    if 'next' in request.GET:
        next_page = request.GET['next']
    if request.user.is_authenticated and next_page is not None:
        return HttpResponseRedirect(next_page)

    if request.user.is_anonymous and "username" in request.POST and "password" in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, "Vaše přihlášení proběhlo úspěšně")
                if next_page is not None:
                    return HttpResponseRedirect(next_page)
            else:
                messages.error(request, "Vás účet není aktivován")
        else:
            messages.error(request, "Neplatné uživatelské jměno nebo heslo")
    return redirect('base:index')


@login_required
def log_out(request):
    logout(request)
    return redirect('base:index')


def registration(request):
    if request.user.is_anonymous:
        form = RegistrationForm(request.POST or None)
        if request.POST and form.is_valid():
            user = IFUser(email=form.cleaned_data['email'],
                          username=form.cleaned_data['nickname'])
            user.set_password(form.cleaned_data['password'])
            # TODO THIS HAS TO BE REMOVED
            user.is_staff = True
            user.is_superuser = True
            # TODO THIS HAS TO BE REMOVED
            user.save()
            login(request, user)

            return redirect('base:index')
        return render(request, 'registration.html', {'form': form})
    else:
        return redirect('base:index')


def site_rules(request):
    return render(request, 'pages/site_rules.html')


def statistics(request):
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


def login_required(request):
    return render(request, 'login_required.html')

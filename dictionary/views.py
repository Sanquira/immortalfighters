from django.shortcuts import render, redirect

# Create your views here.
from base.views import MenuWrapper


def index(request):
    if request.user.is_authenticated:
        return render(request, 'dictionary_base.html', {'menu_attrs': MenuWrapper()})
    else:
        return render(request, 'base.html', {'menu_attrs': MenuWrapper()})


def spells(request):
    return redirect('dictionary:index')


def skills(request):
    return redirect('dictionary:index')


def items(request):
    return redirect('dictionary:index')


def races(request):
    return redirect('dictionary:index')


def professions(request):
    return redirect('dictionary:index')
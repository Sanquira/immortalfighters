from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    if request.user.is_authenticated:
        return render(request, 'logged_base.html', {'menu_attrs': MenuWrapper()})
    else:
        return render(request, 'base.html', {'menu_attrs': MenuWrapper()})


def banners(request):
    return render(request, 'base.html')


class MenuWrapper:

    def __init__(self):
        pass

    pass

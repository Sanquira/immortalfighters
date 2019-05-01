from django.shortcuts import redirect


def races(request):
    return redirect('dictionary:index')

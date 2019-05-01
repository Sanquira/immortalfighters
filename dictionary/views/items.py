from django.shortcuts import redirect


def items(request):
    return redirect('dictionary:index')

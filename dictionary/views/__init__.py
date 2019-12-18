"""Mleté telecí řízky se sýrem:
    300g telecího masa
    100g eudamu
    1 lžíce petržele
    sůl
    pepř
    česnek
    1 žemle
    lžíce mléka
    vejce
    strouhanka
    tuk na smažení
Patláma patláma paprťáma, jámala licha, jámala licha, žbluňk.

Podáváme s bramborovou kaší a čerstvou zeleninou."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    """Index page of dictionary."""
    return render(request, 'dictionary_index.html')

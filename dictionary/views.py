from django.shortcuts import render, redirect

# Create your views here.
from base.views import MenuWrapper
from dictionary.forms import SpellForm
from dictionary.models import Spell, ProfessionLimitation, BaseProfession


def index(request):
    if request.user.is_authenticated:
        return render(request, 'dictionary_base.html', {'menu_attrs': MenuWrapper()})
    else:
        return render(request, 'base.html', {'menu_attrs': MenuWrapper()})


def spells(request):
    return redirect('dictionary:index')


def spell_add(request):
    if request.user.is_authenticated:
        form = SpellForm(request.POST or None)
        if request.POST and form.is_valid():
            spell = Spell(name=form.cleaned_data['name'],
                          mana=form.cleaned_data['mana'],
                          range=form.cleaned_data['range'],
                          cast_time=form.cleaned_data['cast_time'],
                          duration=form.cleaned_data['duration'],
                          note=form.cleaned_data['note'])
            spell.save()
            if form.cleaned_data['profession'] is not None:
                prof = BaseProfession.objects.get(name=form.cleaned_data['profession'])
                limit = ProfessionLimitation(
                    profession=prof,
                    spell=spell,
                    from_level=form.cleaned_data['level']
                )
                limit.save()
            return redirect('dictionary:spells')
        return render(request, 'spell_add.html', {'form': form})
    return redirect('dictionary:spells')


def skills(request):
    return redirect('dictionary:index')


def items(request):
    return redirect('dictionary:index')


def races(request):
    return redirect('dictionary:index')


def professions(request):
    return redirect('dictionary:index')

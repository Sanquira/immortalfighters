from django.db.models.functions import Lower
from django.shortcuts import redirect, render, get_object_or_404

from base.views import MenuWrapper
from dictionary.forms import SpellForm, ProfessionLimitationForm, SpellFormEdit
from dictionary.models import ProfessionLimitation, Spell


def spells(request):
    if request.user.is_authenticated:
        sort = request.GET.get('sort', 'ascend')
        order = request.GET.get('order', 'name')
        if sort == "ascend":
            spell_list = Spell.objects.order_by(Lower(order).asc()).order_by('id')
        elif sort == "descend":
            spell_list = Spell.objects.order_by(Lower(order).desc()).order_by('-id')
        else:
            return redirect('dictionary:index')
        return render(request, 'spells_list.html',
                      {'spell_list': spell_list, 'order': order, 'sort': sort, 'menu_attrs': MenuWrapper()})
    return redirect('base:index')


def spell_add(request):
    if request.user.is_authenticated:
        form_spell = SpellForm(request.POST or None)
        form_pl = ProfessionLimitationForm(request.POST or None)
        if request.POST and form_spell.is_valid() and form_pl.is_valid() and \
                Spell.objects.filter(name=form_spell.cleaned_data['name']).count() == 0:
            form_spell = form_spell.save()
            if form_pl.cleaned_data['profession'] is not None:
                form_pl = form_pl.save(commit=False)
                form_pl.spell = form_spell
                form_pl.save()
            return redirect('dictionary:spells')
        return render(request, 'spell_add.html', {'form_spell': form_spell, 'form_pl': form_pl})
    return redirect('base:index')


def spell_edit(request, pk):
    if request.user.is_authenticated:
        if pk:
            spell = get_object_or_404(Spell, pk=pk)
        else:
            spell = Spell()

        try:
            limitation = ProfessionLimitation.objects.get(spell=spell)
        except ProfessionLimitation.DoesNotExist:
            limitation = ProfessionLimitation()

        form_spell = SpellFormEdit(request.POST or None, instance=spell)
        form_pl = ProfessionLimitationForm(request.POST or None, instance=limitation)
        if request.POST and form_spell.is_valid() and form_pl.is_valid():
            spell = form_spell.save()
            if form_pl.cleaned_data['profession'] is not None:
                limitation = form_pl.save(commit=False)
                limitation.spell = spell
                limitation.save()
            return redirect('dictionary:spells')
        return render(request, 'spell_edit.html', {'pk': pk, 'form_spell': form_spell, 'form_pl': form_pl})
    return redirect('base:index')


def spell_delete(request, pk):
    if request.user.is_authenticated:
        if pk:
            spell = get_object_or_404(Spell, pk=pk)
            spell.delete()
    return redirect('dictionary:spells')

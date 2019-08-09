from django.db.models.functions import Lower
from django.shortcuts import redirect, render, get_object_or_404

from dictionary.forms import SpellForm, ProfessionLimitationForm, SpellFormEdit
from dictionary.models.profession import BaseProfession
from dictionary.models.profession_limitation import ProfessionLimitation
from dictionary.models.spell import Spell


def items(request):
    if not request.user.is_authenticated:
        return redirect('base:index')
    sort = request.GET.get('sort', 'ascend')
    order = request.GET.get('order', 'name')
    
    spells = dict()
    
    for prof in BaseProfession.objects.all():
        if sort == "ascend":
            spell_list = Spell.get_spells_for_profession(prof).order_by(Lower(order).asc(), 'id')
        elif sort == "descend":
            spell_list = Spell.get_spells_for_profession(prof).order_by(Lower(order).desc(), '-id')
        else:
            return redirect('dictionary:index')
        if spell_list.count() > 0:
            spells[prof] = spell_list
    if sort == "ascend":
        spell_list = Spell.get_spells_for_profession(None).order_by(Lower(order).asc(), 'id')
    elif sort == "descend":
        spell_list = Spell.get_spells_for_profession(None).order_by(Lower(order).desc(), '-id')
    else:
        return redirect('dictionary:index')
    if spell_list.count() > 0:
        spells['Nezařazeno'] = spell_list
    
    return render(request, 'spells_list.html', {'spells': spells, 'order': order, 'sort': sort})


def item_item(request, pk=None):
    if not request.user.is_authenticated:
        return redirect('base:index')

    # TODO permission system
    is_editing = True
    
    if pk:
        spell = get_object_or_404(Spell, pk=pk)
        is_adding = False
    else:
        spell = Spell()
        is_adding = True
    
    try:
        limitation = ProfessionLimitation.objects.get(spell=spell)
    except ProfessionLimitation.DoesNotExist:
        limitation = ProfessionLimitation()
    
    if is_adding:
        form_spell = SpellForm(request.POST or None, instance=spell)
    else:
        form_spell = SpellFormEdit(request.POST or None, instance=spell)
    
    form_pl = ProfessionLimitationForm(request.POST or None, instance=limitation)
    if request.POST and form_spell.is_valid() and form_pl.is_valid() and \
            ((is_adding and Spell.objects.filter(name=form_spell.cleaned_data['name']).count() == 0) or not is_adding):
        
        spell = form_spell.save()
        if form_pl.cleaned_data['profession'] is not None:
            limitation = form_pl.save(commit=False)
            limitation.spell = spell
            limitation.save()
        else:
            limitation.delete()
        return redirect('dictionary:spells')
    if is_adding or is_editing:
        return render(request, 'spell_item.html', {'add': is_adding, 'edit': is_editing, 'pk': pk, 'form_spell': form_spell, 'form_pl': form_pl})
    return render(request, 'spell_item.html', {'add': is_adding, 'edit': is_editing, 'pk': pk, 'form_spell': form_spell, 'form_pl': form_pl})


def item_delete(request, pk):
    if request.user.is_authenticated:
        if pk:
            spell = get_object_or_404(Spell, pk=pk)
            spell.delete()
    return redirect('dictionary:spells')

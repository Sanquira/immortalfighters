from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Count, Q
from django.forms import modelformset_factory, formset_factory
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404

from base.views import BaseProfession
from dictionary.forms import SpellForm, ProfessionLimitationForm, SpellFormEdit, BaseProfessionLimitationFormSet, SpellDirectionForm, BaseSpellDirectionFormSet
from dictionary.models.profession_limitation import ProfessionLimitation
from dictionary.models.spell import Spell


@login_required
def spells(request):
    dummy_spell = Spell()
    return render(request, 'spells_list.html', {'dummy_spell': dummy_spell})


def spells_table(request):
    datatables = request.POST
    
    # Ambil draw
    draw = int(datatables.get('draw'))
    # Ambil start
    start = int(datatables.get('start'))
    # Ambil length (limit)
    length = int(datatables.get('length'))
    # Ambil data search
    search = datatables.get('search[value]')
    # Ambil order column
    order = datatables.get('order[0][column]')
    order = datatables.get('columns[' + order + '][data]')
    # Ambil order dir
    orderDir = datatables.get('order[0][dir]')
    
    data = [
        {
            'pk': spell.pk,
            'name': spell.name,
            'disciplines': spell.get_disciplines_str(),
            'profession': prof.name
        } for prof in BaseProfession.objects.all() for spell in
        Spell.get_spells_for_profession(prof).filter(name__contains=search)
    ]
    data.extend(
        {
            'pk': spell.pk,
            'name': spell.name,
            'disciplines': spell.get_disciplines_str(),
            'profession': "Nezařazeno"
        } for spell in Spell.get_spells_for_profession(None).filter(name__contains=search)
    )
    
    data.sort(key=lambda x: x[order], reverse=False if orderDir == "asc" else True)
    data.sort(key=lambda x: x["profession"])
    dataFiltered = len(data)
    del data[:start]
    if length > 0:
        del data[length:]
    
    dataTotal = Spell.objects.aggregate(noRestriction=Count('pk', filter=Q(available_for_professions=None)),
                                        restriction=Count('available_for_professions'))
    return JsonResponse({
        'draw': draw,
        'recordsTotal': dataTotal['noRestriction'] + dataTotal['restriction'],
        'recordsFiltered': dataFiltered,
        'data': data,
    })


def spell_item_view(request, pk):
    spell = get_object_or_404(Spell, pk=pk)
    dirs = spell.get_directions_grouped()
    profs = ProfessionLimitation.objects.filter(spell=spell)
    
    return render(request, 'spell_item_view.html',
                  {'spell': spell, 'dirs': dirs, 'profs': profs})


def spell_edit(request, pk):
    if not request.user.is_authenticated:
        return redirect('base:index')
    
    if pk:
        spell = get_object_or_404(Spell, pk=pk)
        form_spell = SpellFormEdit(request.POST or None, instance=spell)
        is_adding = False
    else:
        spell = Spell()
        form_spell = SpellForm(request.POST or None, instance=spell)
        is_adding = True
    
    ProfessionLimitationFormSet = modelformset_factory(ProfessionLimitation, form=ProfessionLimitationForm,
                                                       formset=BaseProfessionLimitationFormSet, min_num=1,
                                                       validate_min=True, validate_max=True, can_delete=True)
    
    SpellDirectionFormSet = formset_factory(SpellDirectionForm, min_num=0, validate_min=True,
                                            validate_max=True, formset=BaseSpellDirectionFormSet,
                                            can_delete=True)
    
    if request.POST:
        form_profs = ProfessionLimitationFormSet(request.POST, prefix="profs")
        form_dirs = SpellDirectionFormSet(request.POST, prefix="dirs")
        
        if form_spell.is_valid() and form_profs.is_valid() and form_dirs.is_valid():
            
            spell = form_spell.save()
            try:
                form_profs.save_all(spell)
                form_dirs.save_all(spell)
                if is_adding:
                    messages.success(request, 'Nové kouzlo bylo uloženo.')
                else:
                    messages.success(request, "Kouzlo bylo úspěšně editováno")
                return redirect("dictionary:spells")
            except IntegrityError:
                messages.error(request, 'There was an error saving your profile.')
    
    else:
        profs = ProfessionLimitation.objects.filter(spell=spell)
        form_profs = ProfessionLimitationFormSet(queryset=profs, prefix="profs")
        dirs = spell.directions.all()
        form_dirs = SpellDirectionFormSet(initial=[{'direction': obj.pk} for obj in dirs], prefix="dirs")
    
    context = dict()
    context['add'] = is_adding
    context['edit'] = True
    context['pk'] = pk
    context['form_spell'] = form_spell
    context['form_profs'] = form_profs
    context['form_dirs'] = form_dirs
    
    return render(request, 'spell_item.html', context)


def spell_item(request, pk=None):
    if not request.user.is_authenticated:
        return redirect('base:index')
    
    # TODO permission system
    
    if pk:
        return spell_item_view(request, pk)
    else:
        return spell_edit(request, pk)


def spell_delete(request, pk):
    if request.user.is_authenticated:
        if pk:
            # TODO permission system
            spell = get_object_or_404(Spell, pk=pk)
            spell.delete()
    return HttpResponse(status=200)

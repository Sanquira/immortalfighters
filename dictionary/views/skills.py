from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404

from dictionary.forms import SkillForm, SkillFormEdit
from dictionary.models.skill import Skill


@login_required
def skills(request):
    dummy_skill = Skill()
    return render(request, 'skills_list.html', {'dummy_skill': dummy_skill})


def skills_table(request):
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
            'pk': skill.pk,
            'name': skill.name,
            'stat': skill.get_stat_display(),
            'difficulty': skill.get_difficulty_display()
        } for skill in Skill.objects.filter(name__contains=search)
    ]
    
    data.sort(key=lambda x: x[order], reverse=False if orderDir == "asc" else True)
    data.sort(key=lambda x: x["stat"])
    dataFiltered = len(data)
    del data[:start]
    if length > 0:
        del data[length:]
    
    dataTotal = Skill.objects.aggregate(noRestriction=Count('pk'))
    
    return JsonResponse({
        'draw': draw,
        'recordsTotal': dataTotal['noRestriction'],
        'recordsFiltered': dataFiltered,
        'data': data,
    })


def skill_item_view(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    
    return render(request, 'skill_item_view.html',
                  {'skill': skill})


@login_required
def skill_edit(request, pk=None):
    if pk:
        skill = get_object_or_404(Skill, pk=pk)
        form_skill = SkillFormEdit(request.POST or None, instance=skill)
        is_adding = False
    else:
        skill = Skill()
        form_skill = SkillForm(request.POST or None, instance=skill)
        is_adding = True
    
    if request.POST:
        if form_skill.is_valid():
            
            spell = form_skill.save()
            if is_adding:
                messages.success(request, 'Nová dovednost byla uložena.')
            else:
                messages.success(request, "Dovednost byla úspěšně editována")
            return redirect("dictionary:skills")
    
    context = dict()
    context['add'] = is_adding
    context['edit'] = True
    context['pk'] = pk
    context['form_skill'] = form_skill
    
    return render(request, 'skill_item.html', context)


def skill_delete(request, pk):
    if request.user.is_authenticated:
        if pk:
            # TODO permission system
            skill = get_object_or_404(Skill, pk=pk)
            skill.delete()
    return HttpResponse(status=200)

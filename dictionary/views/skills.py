from django.contrib import messages
from django.db.models.functions import Lower
from django.shortcuts import redirect, render, get_object_or_404

from base.models.stat import Stat
from base.views import MenuWrapper
from dictionary.forms import SkillForm, SkillFormEdit
from dictionary.models.skill import Skill


def skills(request):
    if not request.user.is_authenticated:
        return redirect('base:index')
    sort = request.GET.get('sort', 'ascend')
    order = request.GET.get('order', 'name')
    
    skills = dict()
    
    for stat in Stat:
        if sort == "ascend":
            skill_list = Skill.objects.filter(stat=stat.name).order_by(Lower(order).asc(), 'id')
        elif sort == "descend":
            skill_list = Skill.objects.filter(stat=stat.name).order_by(Lower(order).desc(), '-id')
        else:
            return redirect('dictionary:index')
        if skill_list.count() > 0:
            skills[stat] = skill_list
    
    return render(request, 'skill_list.html', {'skills': skills, 'order': order, 'sort': sort, 'menu_attrs': MenuWrapper()})


def skill_item(request, pk=None):
    if not request.user.is_authenticated:
        return redirect('base:index')
    
    # TODO permission system
    is_editing = False
    
    if pk:
        skill = get_object_or_404(Skill, pk=pk)
        is_adding = False
    else:
        skill = Skill()
        is_adding = True
    
    if is_adding:
        form_skill = SkillForm(request.POST or None, instance=skill)
    else:
        form_skill = SkillFormEdit(request.POST or None, instance=skill)
    
    if request.POST and form_skill.is_valid():
        if is_adding and Skill.objects.filter(name=form_skill.cleaned_data['name']).count() == 0:
            form_skill.save()
            messages.success(request, "Skill s ID %(id)s byl přidán" % {'id': pk})
        elif not is_adding:
            form_skill.save()
            messages.success(request, "Skill s ID %(id)s byl úspěšně upraven" % {'id': pk})

        return redirect('dictionary:skills')
    return render(request, 'skill_item.html', {'add': is_adding, 'edit': is_editing, 'pk': pk, 'form_skill': form_skill})


def skill_delete(request, pk):
    if request.user.is_authenticated:
        if pk:
            skill = get_object_or_404(Skill, pk=pk)
            skill.delete()
            messages.success(request, "Skill s ID %(id)s byl smazán" % {'id': pk})
    return redirect('dictionary:skills')

"""Implementation of GenenericView for Spell entity"""
from django.db.models import Count, Q
from django.forms import modelformset_factory, formset_factory
from django.shortcuts import redirect

from dictionary.forms.spell_form import SpellForm, ProfessionLimitationForm, \
    BaseProfessionLimitationFormSet, BaseSpellDirectionFormSet, SpellDirectionForm
from dictionary.models.profession import BaseProfession
from dictionary.models.spell import Spell, ProfessionLimitation
from dictionary.views.generic_view import GenericView


class SpellView(GenericView):
    """Implementation of GenenericView for Spell entity"""
    ProfessionLimitationFormSet = modelformset_factory(ProfessionLimitation, form=ProfessionLimitationForm,
                                                       formset=BaseProfessionLimitationFormSet, min_num=1,
                                                       validate_min=True, validate_max=True, can_delete=True, extra=1)
    
    SpellDirectionFormSet = formset_factory(SpellDirectionForm, min_num=0, validate_min=True,
                                            validate_max=True, formset=BaseSpellDirectionFormSet,
                                            can_delete=True, extra=1)
    
    def __init__(self):
        super().__init__(Spell, SpellForm, 'spell/view.html', 'spell/edit.html')
        self.add_successful_msg = "Nové kouzlo bylo uloženo."
        self.edit_successful_msg = "Kouzlo bylo úspěšně upraveno."
    
    def get_success_response(self):
        return redirect("dictionary:spell")
    
    # pylint: disable=unexpected-keyword-arg
    # Disabled because of queryset in formset.
    def get_default_formset_dict(self, item, is_adding: bool) -> dict:
        ret = dict()
        profs = ProfessionLimitation.objects.filter(spell=item)
        if not is_adding:
            dirs = item.directions.all()
            ret['formset_dirs'] = self.SpellDirectionFormSet(
                initial=[{'direction': obj.pk} for obj in dirs],
                prefix="formset-dir")
        else:
            ret['formset_dirs'] = self.SpellDirectionFormSet(prefix="formset-dir")
        ret['formset_dirs'].title = "Směry magie (automaticky přidá odpovídající obor)"
        ret['formset_profs'] = self.ProfessionLimitationFormSet(queryset=profs, prefix="formset-prof")
        ret['formset_profs'].title = "Omezení povolání"
        return ret
    
    def get_formset_dict(self, post) -> dict:
        ret = dict()
        ret['formset_dirs'] = self.SpellDirectionFormSet(post, prefix="formset-dir")
        ret['formset_dirs'].title = "Směry magie (automaticky přidá odpovídající obor)"
        ret['formset_profs'] = self.ProfessionLimitationFormSet(post, prefix="formset-prof")
        ret['formset_profs'].title = "Omezení povolání"
        return ret
    
    # pylint: disable=duplicate-code
    def get_edit_context(self):
        ret = dict()
        ret['header_includes'] = [
            "includes/formset.html"
        ]
        return ret
    
    def get_view_context(self):
        return {
            'title': "Kouzlo"
        }
    
    def get_data_list(self, search: str):
        data = [
            {
                'pk': spell.pk,
                'profession': prof.name,
                'name': spell.name,
                'directions': spell.get_disciplines_str(),
            } for prof in BaseProfession.objects.all() for spell in
            Spell.get_spells_for_profession(prof).filter(name__contains=search)
        ]
        data.extend(
            {
                'pk': spell.pk,
                'profession': "Nezařazeno",
                'name': spell.name,
                'directions': spell.get_disciplines_str(),
            } for spell in Spell.get_spells_for_profession(None).filter(name__contains=search)
        )
        return data
    
    def get_data_total(self):
        return Spell.objects.aggregate(noRestriction=Count('pk', filter=Q(available_for_professions=None)),
                                       restriction=Count('available_for_professions'))
    
    def get_table_context(self):
        return {
            'columns': [{"data": 'pk', "visible": False},
                        {"data": 'profession', "visible": False},
                        {"data": 'name'},
                        {"data": 'directions'},
                        ],
            'group_column': 1,
            'title': "Kouzla",
            'add_label': "Přidej kouzlo",
        }

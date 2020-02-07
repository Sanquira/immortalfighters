"""Implementation of GenenericView for Beast entity"""
from django.db.models import Count
from django.forms import modelformset_factory, formset_factory
from django.shortcuts import redirect

from dictionary.forms.beast_form import AttackForm, BaseAttackFormSet, \
    MobilityForm, BaseMobilityFormSet, WeaknessForm, BaseWeaknessFormSet, BeastForm
from dictionary.models.beast import Beast, BeastAttack, BeastMobility, BeastWeakness
from dictionary.views.generic_view import GenericView


class BeastView(GenericView):
    """Implementation of GenenericView for Beast entity"""
    AttackFormSet = modelformset_factory(BeastAttack, form=AttackForm, formset=BaseAttackFormSet,
                                         min_num=1, validate_min=True, can_delete=True, extra=1)

    MobilityFormSet = modelformset_factory(BeastMobility, form=MobilityForm, formset=BaseMobilityFormSet,
                                           min_num=1, validate_min=True, can_delete=True, extra=1)

    WeaknessFormSet = formset_factory(WeaknessForm, formset=BaseWeaknessFormSet,
                                      min_num=1, validate_min=True, can_delete=True, extra=1)

    def __init__(self):
        super().__init__(Beast, BeastForm, 'beast/view.html', 'beast/edit.html')
        self.add_successful_msg = "Nová příšera byla uložena."
        self.edit_successful_msg = "Příšera byla úspěšně upravena."

    def get_formset_dict(self, post) -> dict:
        ret = dict()
        ret["attack"] = self.AttackFormSet(post, prefix="formset-attack")
        ret["attack"].title = "Útočná čísla"
        ret["mobility"] = self.MobilityFormSet(post, prefix="formset-mobility")
        ret["mobility"].title = "Pohyblivosti"
        ret["weakness"] = self.WeaknessFormSet(post, prefix="formset-weakness")
        ret["weakness"].title = "Zranitelnosti"
        return ret

    # pylint: disable=unexpected-keyword-arg
    # Disabled because of queryset in formset.
    def get_default_formset_dict(self, item, is_adding: bool) -> dict:
        ret = dict()
        ret["attack"] = self.AttackFormSet(queryset=item.beastattack_set.all(), prefix="formset-attack")
        ret["attack"].title = "Útočná čísla"
        ret["mobility"] = self.MobilityFormSet(queryset=item.beastmobility_set.all(), prefix="formset-mobility")
        ret["mobility"].title = "Pohyblivosti"
        if not is_adding:
            ret["weakness"] = self.WeaknessFormSet(
                initial=[{'weakness': obj.pk} for obj in BeastWeakness.objects.filter(beast=item)],
                prefix="formset-weakness")
        else:
            ret["weakness"] = self.WeaknessFormSet(prefix="formset-weakness")
        ret["weakness"].title = "Zranitelnosti"
        return ret

    def get_success_response(self):
        return redirect("dictionary:beast")

    # pylint: disable=duplicate-code
    def get_edit_context(self):
        return {
            'header_includes': [
                "includes/formset.html"
            ]
        }

    def get_view_context(self):
        return {
            'title': "Příšera",
            'header_includes': [
                "includes/tooltipster.html"
            ]
        }

    def get_data_list(self, search: str):
        return [
            {
                'pk': beast.pk,
                'category': beast.category.name,
                'name': beast.name,
                'life': beast.life,
                'attack': beast.beastattack_set.all()[0].dmg,
                'defense': beast.defense,
            } for beast in Beast.objects.filter(name__contains=search)
        ]

    def get_data_total(self):
        return Beast.objects.aggregate(noRestriction=Count('pk'))

    def get_table_context(self):
        return {
            'columns': [{"data": 'pk', "visible": False},
                        {"data": 'category', "visible": False},
                        {"data": 'name'},
                        {"data": 'life'},
                        {"data": 'attack'},
                        {"data": 'defense'},
                        ],
            'group_column': 1,
            'title': "Příšery",
            'add_label': "Přidej příšeru",
        }

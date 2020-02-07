"""Implementation of GenericView for Skill entity"""
from django.db.models import Count
from django.shortcuts import redirect

from dictionary.forms.skill_form import SkillForm
from dictionary.models.skill import Skill
from dictionary.views.generic_view import GenericView


class SkillView(GenericView):
    """Implementation of GenericView for Skill entity"""

    def __init__(self):
        super().__init__(Skill, SkillForm, 'skill/view.html', 'skill/edit.html')
        self.add_successful_msg = "Nová dovednost byla uložena."
        self.edit_successful_msg = "Dovednost byla úspěšně upravena."

    def get_success_response(self):
        return redirect("dictionary:skill")

    def get_view_context(self):
        return {
            'title': "Dovednost"
        }

    def get_data_list(self, search: str):
        return [
            {
                'pk': skill.pk,
                'name': skill.name,
                'stat': skill.stat.name,
                'difficulty': skill.difficulty.name
            } for skill in Skill.objects.filter(name__contains=search)
        ]

    def get_data_total(self):
        return Skill.objects.aggregate(noRestriction=Count('pk'))

    def get_table_context(self):
        return {
            'columns': [{"data": 'pk', "visible": False},
                        {"data": 'stat', "visible": False},
                        {"data": 'name'},
                        {"data": 'difficulty'},
                        ],
            'group_column': 1,
            'title': "Dovednosti",
            'add_label': "Přidej dovednost",
        }

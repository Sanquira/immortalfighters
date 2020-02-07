"""Form classes for Skill entity."""
from django.forms import ModelForm

from dictionary.models.skill import Skill


class SkillForm(ModelForm):
    """Form for basic Skill entity"""

    class Meta:
        model = Skill
        fields = '__all__'

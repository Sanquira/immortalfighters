from django import forms
from django.forms import ModelForm

from dictionary.models import BaseProfession, ProfessionLimitation
from dictionary.models.spell import Spell


class SpellFormEdit(ModelForm):
    class Meta:
        model = Spell
        exclude = ('available_for_professions',)


class SpellForm(SpellFormEdit):
    def clean_name(self):
        clname = self.cleaned_data.get('name')
        if Spell.objects.filter(name=clname).exists():
            raise forms.ValidationError('Kouzlo s tímto jménem už existuje.')
        return clname


class ProfessionLimitationForm(ModelForm):
    profession = forms.ModelChoiceField(required=False, queryset=BaseProfession.objects.all(), label="Povolání")

    class Meta:
        model = ProfessionLimitation
        exclude = ('spell',)

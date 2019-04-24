from django import forms

from dictionary.models import BaseProfession
from dictionary.models.spell import Spell


class SpellForm(forms.Form):
    name = forms.CharField(label="Jméno kouzla", max_length=128)
    mana = forms.CharField(label="Mana", max_length=128)
    range = forms.CharField(label="Dosah", max_length=32)
    cast_time = forms.CharField(label="Vyvolání", max_length=32)
    duration = forms.CharField(label="Trvání", max_length=32)
    note = forms.CharField(widget=forms.Textarea, label="Popis")
    profession = forms.ModelChoiceField(label="Povolání", queryset=BaseProfession.objects.all())
    level = forms.IntegerField(label="Od úrovně", min_value=1)

    def clean_name(self):
        clname = self.cleaned_data.get('name')
        if Spell.objects.filter(name=clname).exists():
            raise forms.ValidationError('Kouzlo s tímto jménem už existuje.')
        return clname

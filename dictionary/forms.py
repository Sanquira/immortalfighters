from django import forms
from django.db import transaction, IntegrityError
from django.forms import ModelForm, BaseModelFormSet

from dictionary.models.profession import BaseProfession
from dictionary.models.profession_limitation import ProfessionLimitation
from dictionary.models.skill import Skill
from dictionary.models.spell import Spell


# Spells
class SpellFormEdit(ModelForm):
    class Meta:
        model = Spell
        exclude = ('directions', 'available_for_professions',)


class SpellForm(SpellFormEdit):
    def clean_name(self):
        clname = self.cleaned_data.get('name')
        if Spell.objects.filter(name=clname).exists():
            raise forms.ValidationError('Kouzlo s tímto jménem už existuje.')
        return clname


class ProfessionLimitationForm(ModelForm):
    profession = forms.ModelChoiceField(required=True, queryset=BaseProfession.objects.all(), label="Povolání")

    class Meta:
        model = ProfessionLimitation
        exclude = ('spell',)

    def get_profession_name(self):
        """ returns the name of the selected profession """
        try:
            return BaseProfession.objects.get(id=self.initial['profession_id']).name
        except:
            return None


class BaseProfessionLimitationFormSet(BaseModelFormSet):
    def clean(self):
        if any(self.errors):
            return

        if len(self.forms) == 0:
            raise forms.ValidationError(
                'Musí být vytvořeno aspon jedno povolání.',
                code='no_profession'
            )

        profs = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                prof = form.cleaned_data['profession']

                # TODO from_level empty, non-number value check??
                if prof in profs:
                    duplicates = True
                profs.append(prof)
                if duplicates:
                    raise forms.ValidationError(
                        'Duplicita povolání není povolena.',
                        code='duplicate_profession'
                    )

    def save_all(self, spell):
        with transaction.atomic():
            for form_prof in self:
                prof = form_prof.save(commit=False)
                prof.spell = spell
                prof.save()


# Skills
class SkillFormEdit(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'


class SkillForm(SkillFormEdit):
    def clean_name(self):
        clname = self.cleaned_data.get('name')
        if Skill.objects.filter(name=clname).exists():
            raise forms.ValidationError('Dovednost s tímto jménem už existuje.')
        return clname

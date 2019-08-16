from django import forms
from django.db import transaction
from django.forms import ModelForm, BaseModelFormSet, Form, BaseFormSet

from base.fields import EmptyChoiceField
from dictionary.models.profession import BaseProfession
from dictionary.models.profession_limitation import ProfessionLimitation
from dictionary.models.skill import Skill
from dictionary.models.spell import Spell, SpellDirection


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
    
    def clean_profession(self):
        data = self.cleaned_data['profession']
        
        return data


class BaseProfessionLimitationFormSet(BaseModelFormSet):
    def clean(self):
        if any(self.errors):
            return
        profs = []
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            
            if form.cleaned_data and 'profession' in form.cleaned_data:
                prof = form.cleaned_data['profession']
                # TODO from_level empty, non-number value check??
                if prof in profs:
                    raise forms.ValidationError(
                        'Duplicita povolání není povolena.',
                        code='duplicate_profession'
                    )
                profs.append(prof)
    
    def save_all(self, spell):
        with transaction.atomic():
            instances = self.save(commit=False)
            for instance in instances:
                instance.spell = spell
                instance.save()
            for instance in self.deleted_objects:
                instance.delete()


class SpellDirectionForm(Form):
    direction = EmptyChoiceField(required=False, label="Směr magie", empty_label='---------',
                                 choices=[(obj.pk, obj.get_form_label()) for obj in SpellDirection.objects.all()])


class BaseSpellDirectionFormSet(BaseFormSet):
    
    def clean(self):
        if any(self.errors):
            return
        dirs = []
        for form in self.forms:
            if self._should_delete_form(form):
                continue
            
            if form.cleaned_data and 'direction' in form.cleaned_data:
                dir = form.cleaned_data['direction']
                if dir in dirs:
                    raise forms.ValidationError(
                        'Duplicita směrů není povolena.',
                        code='duplicate_direction'
                    )
                dirs.append(dir)
    
    def save_all(self, spell):
        if not self.has_changed():
            return
        with transaction.atomic():
            spell.directions.clear()
            for form in self.forms:
                if 'direction' not in form.cleaned_data:
                    continue
                if form.cleaned_data['DELETE'] == True:
                    continue
                dir = SpellDirection.objects.get(pk=form.cleaned_data['direction'])
                spell.directions.add(dir)
    
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

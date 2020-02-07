"""Form classes for Spell entity"""
from django import forms
from django.db import transaction
from django.forms import ModelForm, BaseModelFormSet, Form, BaseFormSet, ChoiceField

from dictionary.models.spell import Spell, SpellDirection, ProfessionLimitation


class SpellForm(ModelForm):
    """Form for basic Spell entity"""

    class Meta:
        model = Spell
        fields = ('name',
                  'mana',
                  'range',
                  'scope',
                  'cast_time',
                  'duration',
                  'note',
                  )


class ProfessionLimitationForm(ModelForm):
    """Form for ProfessionLimitation in Spell"""

    class Meta:
        model = ProfessionLimitation
        fields = ('profession',
                  'from_level',
                  )


class BaseProfessionLimitationFormSet(BaseModelFormSet):
    """Formset of ProfessionLimitation in Spell"""

    def clean(self):
        if any(self.errors):
            return
        profs = []
        for form in self.forms:
            if self._should_delete_form(form):
                continue

            if form.cleaned_data and 'profession' in form.cleaned_data:
                prof = form.cleaned_data['profession']
                if prof in profs:
                    raise forms.ValidationError(
                        'Duplicita povolání není povolena.',
                        code='duplicate_profession'
                    )
                profs.append(prof)

    def save_all(self, spell):
        """Saves formset. It has to be valid."""
        with transaction.atomic():
            instances = self.save(commit=False)
            for instance in instances:
                instance.spell = spell
                instance.save()
            for instance in self.deleted_objects:
                instance.delete()


def get_direction_choices():
    """Return choices for Directions"""
    ret = [(obj.pk, obj.get_form_label()) for obj in SpellDirection.objects.all()]
    ret.insert(0, (None, '----------'))
    return ret


class SpellDirectionForm(Form):
    """Form for Direction in Spell"""
    direction = ChoiceField(required=False,
                            label=Spell._meta.get_field('directions').related_model._meta.verbose_name,
                            choices=get_direction_choices)


class BaseSpellDirectionFormSet(BaseFormSet):
    """Formset of Direction in Spell"""

    def clean(self):
        if any(self.errors):
            return
        frms = []
        for form in self.forms:
            if self._should_delete_form(form):
                continue

            if form.cleaned_data and 'direction' in form.cleaned_data:
                frm = form.cleaned_data['direction']
                if frm in frms:
                    raise forms.ValidationError(
                        'Duplicita směrů není povolena.',
                        code='duplicate_direction'
                    )
                frms.append(frm)

    def save_all(self, spell):
        """Saves formset. It has to be valid."""
        if not self.has_changed():
            return
        with transaction.atomic():
            spell.directions.clear()
            for form in self.forms:
                if 'direction' not in form.cleaned_data:
                    continue
                if form.cleaned_data['DELETE']:
                    continue
                drc = SpellDirection.objects.get(pk=form.cleaned_data['direction'])
                spell.directions.add(drc)

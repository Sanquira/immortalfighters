"""Form classes for Beast entity."""
from django import forms
from django.db import transaction
from django.forms import ModelForm, Form, BaseFormSet, BaseModelFormSet, ChoiceField

from dictionary.models.beast import Beast, BeastWeakness, BeastAttack, BeastMobility


class BeastForm(ModelForm):
    """Form for basic Beast entity"""

    class Meta:
        model = Beast
        fields = ('name',
                  'life',
                  'defense',
                  'resist',
                  'size',
                  'fury',
                  'endurance',
                  'inteligence',
                  'treasure',
                  'exp',
                  'note',
                  'note_pj',
                  'powers',
                  'category',
                  )


def get_weakness_choices():
    """Return choices for Weakness"""
    ret = [(obj.pk, obj.group) for obj in BeastWeakness.objects.all()]
    ret.insert(0, (None, '-'))
    return ret


class WeaknessForm(Form):
    """Form for Weakness in Beast"""
    weakness = ChoiceField(required=False,
                           label=Beast._meta.get_field('weakness').verbose_name,
                           choices=get_weakness_choices)


class BaseWeaknessFormSet(BaseFormSet):
    """Formset of WeaknessForm"""

    def clean(self):
        if any(self.errors):
            return
        frms = []
        for form in self.forms:
            if self._should_delete_form(form):
                continue

            if form.cleaned_data and 'weakness' in form.cleaned_data:
                frm = form.cleaned_data['weakness']
                if frm in frms:
                    raise forms.ValidationError(
                        'Duplicita zranitelností není povolena.',
                        code='duplicate_weakness'
                    )
                frms.append(frm)

    def save_all(self, beast):
        """Saves formset. It has to be valid."""
        if not self.has_changed():
            return
        with transaction.atomic():
            beast.weakness.clear()
            for form in self.forms:
                if 'weakness' not in form.cleaned_data:
                    continue
                if form.cleaned_data['DELETE']:
                    continue
                wkn = BeastWeakness.objects.get(pk=form.cleaned_data['weakness'])
                beast.weakness.add(wkn)


class AttackForm(ModelForm):
    """Form for Attack in Beast"""

    class Meta:
        model = BeastAttack
        fields = ('dmg',)


class BaseAttackFormSet(BaseModelFormSet):
    """Formset of AttackForm"""

    def save_all(self, beast):
        """Saves formset. It has to be valid."""
        with transaction.atomic():
            instances = self.save(commit=False)
            for instance in instances:
                instance.beast = beast
                instance.save()
            for instance in self.deleted_objects:
                instance.delete()


class MobilityForm(ModelForm):
    """Form for Mobility in Beast"""

    class Meta:
        model = BeastMobility
        fields = ('mob',)


class BaseMobilityFormSet(BaseModelFormSet):
    """Formset of MobilityForm"""

    def save_all(self, beast):
        """Saves formset. It has to be valid."""
        with transaction.atomic():
            instances = self.save(commit=False)
            for instance in instances:
                instance.beast = beast
                instance.save()
            for instance in self.deleted_objects:
                instance.delete()

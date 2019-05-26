from django.db import models
from markdownx.models import MarkdownxField

from dictionary.models.profession import BaseProfession


class Spell(models.Model):
    name = models.CharField(max_length=128, null=False, default="Nové kouzlo", verbose_name="Jméno kouzla")
    mana = models.CharField(max_length=128, null=True, verbose_name="Mana")
    range = models.CharField(max_length=128, null=True, verbose_name="Dosah")
    scope = models.CharField(max_length=128, null=True, verbose_name="Rozsah")
    cast_time = models.CharField(max_length=128, null=True, verbose_name="Vyvolání")
    duration = models.CharField(max_length=128, null=True, verbose_name="Trvání")
    note = MarkdownxField(null=True,verbose_name="Popis")
    discipline = models.ForeignKey('SpellDiscipline', on_delete=models.CASCADE, null=True, blank=True,
                                   verbose_name="Obor magie")

    available_for_professions = models.ManyToManyField(BaseProfession, through='ProfessionLimitation')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kouzlo"
        verbose_name_plural = "Kouzla"


class SpellDiscipline(models.Model):
    name = models.CharField(max_length=64, null=False, default="Nový obor magie", verbose_name="Název oboru magie")
    label = models.CharField(max_length=4, null=False, default="NO", verbose_name="Zkratka")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Obor magie"
        verbose_name_plural = "Obory magie"


def initialize_spell_disciplines(apps, schema_editor):
    """To init spell disciplines, just call this method in migration.
    Like this:
        migrations.RunPython(spell.initialize_spell_disciplines)
    Dont forget to import.
    """
    SpellDiscipline(name="Časoprostorová magie", label="ČP").save()
    SpellDiscipline(name="Energetická útočná magie", label="EU").save()
    SpellDiscipline(name="Energetická ochranná magie", label="EO").save()
    SpellDiscipline(name="Iluzionistická magie", label="IL").save()
    SpellDiscipline(name="Materiální magie", label="MA").save()
    SpellDiscipline(name="Vitální magie", label="VI").save()
    SpellDiscipline(name="Psychická magie", label="PS").save()
    SpellDiscipline(name="Magie poznávání", label="PO").save()

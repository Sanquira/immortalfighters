"""Module for Spell entity and corresponding objects."""
from django.db import models
from markdownx.models import MarkdownxField

from base.models.profession import BaseProfession


class SpellDiscipline(models.Model):
    """Model for Spell discipline."""
    name = models.CharField(max_length=64, null=False, default="Nový obor magie", verbose_name="Obor magie")
    label = models.CharField(max_length=4, null=False, default="NO", verbose_name="Zkratka")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Obor magie"
        verbose_name_plural = "Obory magie"


class SpellDirection(models.Model):
    """Model for Spell direction."""
    discipline = models.ForeignKey(SpellDiscipline, on_delete=models.CASCADE, verbose_name="Obor magie")
    name = models.CharField(max_length=64, null=False, default="Nový směr magie", verbose_name="Směr magie")
    correct = models.SmallIntegerField(default=0, verbose_name="Oprava")
    
    def get_form_label(self):
        """Returns string concatenated from name of direction and name of discipline."""
        return self.name + " (" + self.discipline.name + ")"
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Směr magie"
        verbose_name_plural = "Směry magie"


class Spell(models.Model):
    """Model for Spell."""
    name = models.CharField(max_length=128, null=False, unique=True,
                            default="Nové kouzlo", verbose_name="Jméno kouzla")
    mana = models.CharField(max_length=128, null=True, verbose_name="Mana")
    range = models.CharField(max_length=128, null=True, verbose_name="Dosah")
    scope = models.CharField(max_length=128, null=True, verbose_name="Rozsah")
    cast_time = models.CharField(max_length=128, null=True, verbose_name="Vyvolání")
    duration = models.CharField(max_length=128, null=True, verbose_name="Trvání")
    note = MarkdownxField(null=True, verbose_name="Popis")
    directions = models.ManyToManyField(SpellDirection, verbose_name="Obory magie")
    
    available_for_professions = models.ManyToManyField(BaseProfession, through='ProfessionLimitation',
                                                       verbose_name="Povolání")
    
    def get_directions_str(self):
        """Returns string concatenated from all Spell directions."""
        return ", ".join(d.__str__() for d in self.directions.all())
    
    def get_disciplines(self):
        """Returns disciplines on Spell."""
        discs = []
        for disc in self.directions.all():
            if disc.discipline not in discs:
                discs.append(disc.discipline)
        return discs
    
    def get_directions_grouped(self):
        """Group directions on Spell by disciplines."""
        discs = {}
        for dirc in self.directions.all():
            if dirc.discipline not in discs:
                discs[dirc.discipline] = list()
            discs[dirc.discipline].append(dirc)
        return discs
    
    def get_disciplines_str(self):
        """Returns string concatenated from all Spell disciplines."""
        return ", ".join(p.name for p in self.get_disciplines())
    
    @staticmethod
    def get_spells_for_profession(prof: 'BaseProfession' = None):
        """Returns Spells which are available for profession."""
        if prof:
            return Spell.objects.filter(available_for_professions=prof)
        return Spell.objects.filter(available_for_professions=None)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Kouzlo"
        verbose_name_plural = "Kouzla"


class ProfessionLimitation(models.Model):
    """Model for Spell profession limitation."""
    spell = models.ForeignKey(Spell, on_delete=models.CASCADE, verbose_name="Kouzlo")
    profession = models.ForeignKey(BaseProfession, on_delete=models.CASCADE, verbose_name="Povolání")
    from_level = models.PositiveSmallIntegerField(default=1, verbose_name="Od úrovně")
    
    def __str__(self):
        return self.profession.name + " - " + self.spell.name
    
    class Meta:
        verbose_name = "Povolání - kouzlo omezení"
        verbose_name_plural = verbose_name


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
    
    initialize_spell_directions(apps, schema_editor)


# pylint: disable=too-many-statements
def initialize_spell_directions(apps, schema_editor):
    """To init spell directions, just call this method in migration.
    Like this:
        migrations.RunPython(spell.initialize_spell_directions)
    Dont forget to import.
    """
    if SpellDirection.objects.count() != 0:
        return
    if SpellDiscipline.objects.count() == 0:
        initialize_spell_disciplines(apps, schema_editor)
    SpellDirection(name="Zrychlení toku času", discipline=SpellDiscipline.objects.filter(label="ČP")[0],
                   correct=-35).save()
    SpellDirection(name="Zpomalení toku času", discipline=SpellDiscipline.objects.filter(label="ČP")[0],
                   correct=-35).save()
    SpellDirection(name="Zastavení toku času", discipline=SpellDiscipline.objects.filter(label="ČP")[0],
                   correct=-53).save()
    SpellDirection(name="Vrácení toku času zpět", discipline=SpellDiscipline.objects.filter(label="ČP")[0],
                   correct=-95).save()
    SpellDirection(name="Posun prostorem", discipline=SpellDiscipline.objects.filter(label="ČP")[0], correct=-20).save()
    SpellDirection(name="Posun prostorem v nulovém čase", discipline=SpellDiscipline.objects.filter(label="ČP")[0],
                   correct=-40).save()
    SpellDirection(name="Postavení prostoru mimo čas", discipline=SpellDiscipline.objects.filter(label="ČP")[0],
                   correct=-60).save()
    
    SpellDirection(name="Prostý výboj", discipline=SpellDiscipline.objects.filter(label="EU")[0], correct=+10).save()
    SpellDirection(name="Zpomalený výboj", discipline=SpellDiscipline.objects.filter(label="EU")[0], correct=-10).save()
    SpellDirection(name="Zrychlený výboj (blesky)", discipline=SpellDiscipline.objects.filter(label="EU")[0],
                   correct=+5).save()
    SpellDirection(name="Zrychlený výboj s efektem (blesky průrazné)",
                   discipline=SpellDiscipline.objects.filter(label="EU")[0], correct=-25).save()
    SpellDirection(name="Úder", discipline=SpellDiscipline.objects.filter(label="EU")[0], correct=-15).save()
    SpellDirection(name="Proud energie", discipline=SpellDiscipline.objects.filter(label="EU")[0], correct=-15).save()
    SpellDirection(name="Naváděný výboj", discipline=SpellDiscipline.objects.filter(label="EU")[0], correct=-35).save()
    SpellDirection(name="Rušivý výboj", discipline=SpellDiscipline.objects.filter(label="EU")[0], correct=-55).save()
    
    SpellDirection(name="Iluze smyslové - zrakové", discipline=SpellDiscipline.objects.filter(label="IL")[0],
                   correct=+6).save()
    SpellDirection(name="Iluze smyslové - sluchové", discipline=SpellDiscipline.objects.filter(label="IL")[0],
                   correct=+3).save()
    SpellDirection(name="Iluze smyslové - hmatové", discipline=SpellDiscipline.objects.filter(label="IL")[0],
                   correct=-5).save()
    SpellDirection(name="Iluze smyslové - čichové", discipline=SpellDiscipline.objects.filter(label="IL")[0],
                   correct=-12).save()
    SpellDirection(name="Iluze smyslové - chuťové", discipline=SpellDiscipline.objects.filter(label="IL")[0],
                   correct=-9).save()
    SpellDirection(name="Iluze smyslové - úplné smyslové", discipline=SpellDiscipline.objects.filter(label="IL")[0],
                   correct=-22).save()
    SpellDirection(name="Iluze tělesné", discipline=SpellDiscipline.objects.filter(label="IL")[0], correct=-35).save()
    SpellDirection(name="Iluze komplexní", discipline=SpellDiscipline.objects.filter(label="IL")[0], correct=-45).save()
    
    SpellDirection(name="Přeměna anorganické hmoty na anorganickou",
                   discipline=SpellDiscipline.objects.filter(label="MA")[0], correct=-20).save()
    SpellDirection(name="Přeměna anorganické hmoty na organickou",
                   discipline=SpellDiscipline.objects.filter(label="MA")[0], correct=-68).save()
    SpellDirection(name="Přeměna organické hmoty na organickou",
                   discipline=SpellDiscipline.objects.filter(label="MA")[0], correct=-35).save()
    SpellDirection(name="Přeměna organické hmoty na anorganickou",
                   discipline=SpellDiscipline.objects.filter(label="MA")[0], correct=-48).save()
    SpellDirection(name="Změna skupenství hmoty", discipline=SpellDiscipline.objects.filter(label="MA")[0],
                   correct=-12).save()
    SpellDirection(name="Změna struktury hmoty", discipline=SpellDiscipline.objects.filter(label="MA")[0],
                   correct=-32).save()
    SpellDirection(name="Vytváření anorganické hmoty", discipline=SpellDiscipline.objects.filter(label="MA")[0],
                   correct=-30).save()
    SpellDirection(name="Vytváření organické hmoty", discipline=SpellDiscipline.objects.filter(label="MA")[0],
                   correct=-45).save()
    
    SpellDirection(name="Odebírání životní síly - odebírání úrovně",
                   discipline=SpellDiscipline.objects.filter(label="VI")[0], correct=-75).save()
    SpellDirection(name="Odebírání životní síly - snížení hranice životů",
                   discipline=SpellDiscipline.objects.filter(label="VI")[0], correct=-95).save()
    SpellDirection(name="Odebírání magenergie", discipline=SpellDiscipline.objects.filter(label="VI")[0],
                   correct=-50).save()
    SpellDirection(name="Navrácení životní síly - navrácení ztracené úrovně",
                   discipline=SpellDiscipline.objects.filter(label="VI")[0], correct=-80).save()
    SpellDirection(name="Navrácení životní síly - Vracení hranice životů",
                   discipline=SpellDiscipline.objects.filter(label="VI")[0], correct=-75).save()
    SpellDirection(name="Manipulace s nemrtvými - přidávání neživotů",
                   discipline=SpellDiscipline.objects.filter(label="VI")[0], correct=-35).save()
    SpellDirection(name="Manipulace s nemrtvými - ubírání neživotů",
                   discipline=SpellDiscipline.objects.filter(label="VI")[0], correct=-25).save()
    SpellDirection(name="Přenášení životní síly - přenášení životů",
                   discipline=SpellDiscipline.objects.filter(label="VI")[0], correct=-60).save()
    SpellDirection(name="Manipulace s vlastnostmi", discipline=SpellDiscipline.objects.filter(label="VI")[0],
                   correct=-65).save()
    SpellDirection(name="Přenášení vědomí", discipline=SpellDiscipline.objects.filter(label="VI")[0],
                   correct=-82).save()
    
    SpellDirection(name="Očarování působící na myšlenky", discipline=SpellDiscipline.objects.filter(label="PS")[0],
                   correct=-35).save()
    SpellDirection(name="Očarování působící na myšlenky a tělo",
                   discipline=SpellDiscipline.objects.filter(label="PS")[0], correct=-53).save()
    SpellDirection(name="Komplexní očarování", discipline=SpellDiscipline.objects.filter(label="PS")[0],
                   correct=-45).save()
    
    SpellDirection(name="Ochrana před fyzickým útokem", discipline=SpellDiscipline.objects.filter(label="EO")[0],
                   correct=-12).save()
    SpellDirection(name="Ochrana před magií", discipline=SpellDiscipline.objects.filter(label="EO")[0],
                   correct=-40).save()
    SpellDirection(name="Ochrana před mentálním útokem", discipline=SpellDiscipline.objects.filter(label="EO")[0],
                   correct=-60).save()
    SpellDirection(name="Komplexní ochrana", discipline=SpellDiscipline.objects.filter(label="EO")[0],
                   correct=-72).save()
    
    SpellDirection(name="Transformace dostupné informace", discipline=SpellDiscipline.objects.filter(label="PO")[0],
                   correct=-40).save()
    SpellDirection(name="Získávání smyslových informací - zrakové či sluchové",
                   discipline=SpellDiscipline.objects.filter(label="PO")[0], correct=-25).save()
    SpellDirection(name="Získávání smyslových informací - ostatní",
                   discipline=SpellDiscipline.objects.filter(label="PO")[0], correct=-28).save()
    SpellDirection(name="Získávání smyslových informací - komplexní",
                   discipline=SpellDiscipline.objects.filter(label="PO")[0], correct=-45).save()
    SpellDirection(name="Získávání mentální informace", discipline=SpellDiscipline.objects.filter(label="PO")[0],
                   correct=-55).save()
    SpellDirection(name="Získávání nedostupných informací", discipline=SpellDiscipline.objects.filter(label="PO")[0],
                   correct=-42).save()

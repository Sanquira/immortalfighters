"""Module for Beast entity and corresponding objects."""
from django.conf import settings
from django.contrib import admin
from django.db import models
from markdownx.models import MarkdownxField

from base.models.sizes import CreatureSize


class BeastWeakness(models.Model):
    """Model for Beast weakness."""
    group = models.CharField(max_length=16, null=False, default='A', verbose_name="Skupina")
    note = models.TextField(null=True, verbose_name="Popis")

    def get_form_label(self):
        """Returns string concatenated from group and note."""
        return self.group + " - " + self.note

    def __str__(self):
        return self.group

    class Meta:
        verbose_name = "Zranitelnost"
        verbose_name_plural = "Zranitelnosti"
        ordering = ['group']


class BeastCategory(models.Model):
    """Model for Beast category."""
    name = models.CharField(max_length=64, null=False, default="Příšera", verbose_name="Jméno kategorie")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kategorie"
        verbose_name_plural = verbose_name
        ordering = ['name']


class Beast(models.Model):
    """Model for Beast."""
    name = models.CharField(max_length=128, null=False, unique=True,
                            default="Nová příšera", verbose_name="Jméno příšery")
    life = models.CharField(max_length=128, null=True, verbose_name="Životaschopnost")
    # attack
    defense = models.CharField(max_length=128, null=True, verbose_name="Obranné číslo")
    resist = models.SmallIntegerField(null=False, default=0, verbose_name="Odolnost")
    size = models.ForeignKey(CreatureSize, on_delete=models.CASCADE, verbose_name="Velikost")
    fury = models.PositiveSmallIntegerField(null=False, default=0, verbose_name="Bojovnost")
    weakness = models.ManyToManyField(BeastWeakness, verbose_name="Zranitelnost")
    # mobility
    endurance = models.SmallIntegerField(null=False, default=0, verbose_name="Vytrvalost")
    inteligence = models.PositiveSmallIntegerField(null=False, default=1, verbose_name="Inteligence")
    treasure = models.CharField(max_length=128, null=True, blank=True, verbose_name="Poklad")
    exp = models.PositiveIntegerField(null=False, default=0, verbose_name="Zkušenosti")
    note = MarkdownxField(null=True, verbose_name="Popis")
    note_pj = MarkdownxField(null=True, blank=True, verbose_name="Popis pro PJ")
    powers = MarkdownxField(null=True, blank=True, verbose_name="Zvláštní schopnosti")
    category = models.ForeignKey(BeastCategory, on_delete=models.CASCADE, verbose_name="Kategorie")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Příšera"
        verbose_name_plural = "Příšery"


class BeastAttack(models.Model):
    """Model for Beast attack."""
    beast = models.ForeignKey(Beast, on_delete=models.CASCADE)
    dmg = models.CharField(max_length=128, null=False, default='', verbose_name="Útočné číslo")

    def __str__(self):
        return self.beast.name + " - " + self.dmg

    class Meta:
        verbose_name = "Útočné číslo"
        verbose_name_plural = "Útočná čísla"


class BeastMobility(models.Model):
    """Model for Beast mobility."""
    beast = models.ForeignKey(Beast, on_delete=models.CASCADE)
    mob = models.SmallIntegerField(null=False, default=0, verbose_name="Pohyblivost")

    def __str__(self):
        return self.beast.name + " - " + str(self.mob)

    class Meta:
        verbose_name = "Pohyblivost"
        verbose_name_plural = "Pohyblivosti"


# pylint: disable=unused-argument,line-too-long
def init_weakness(apps, schema_editor):
    """To init weaknesses, just call this method in migration.
        Like this:
            migrations.RunPython(skill.init_weakness)
        Dont forget to import.
        """
    BeastWeakness(group='A', note="Zápas.").save()
    BeastWeakness(group='B', note="Obyčejná zbraň- Také útok naplocho, boj beze zbraně, pád z výšky.").save()
    BeastWeakness(group='C', note="Kouzelná zbraň.").save()
    BeastWeakness(group='C+', note="Kouzelná zbraň s útočným démonem proti magickým tvorům.").save()
    BeastWeakness(group='D', note="Stříbrná zbraň.").save()
    BeastWeakness(group='D+', note="Zbraň z ušlechtilých kovů (zlato, stříbro, atp.).").save()
    BeastWeakness(group='E', note="Svěcená voda.").save()
    BeastWeakness(group='F', note="Vlčí mor.").save()
    BeastWeakness(group='G', note="Ohnivá hlína, rachejtle či hořící olej, mráz.").save()
    BeastWeakness(group='H', note="Jed, kyselina, alchymistické lektvary, protijedy.").save()
    BeastWeakness(group='I',
                  note="1. skupina kouzel (hraničářská) - úder varování, úder zloby, úder nenávisti, uzdrav lehká zranění, uzdrav těžká zranění, uzdrav nemocného, ošetři zranění chladem, ošetři zranění kyselinou, ošetři zranění ohněm, neutralizuj jed, odstraň únavu.").save()
    BeastWeakness(group='J',
                  note="2. skupina kouzel (útočná) - modré, zelené, černé, fialové, rudé, žluté, bílé a bledé blesky; všechny typy kulových a průrazných blesků, sršatec, temný úder.").save()
    BeastWeakness(group='K',
                  note="3. skupina kouzel (ohnivá a mrazivá) - nebezpečné ovoce, oheň, ohnivý déšť, chlad hvězd, ledový blesk, lomeny plamen, ohnivý bič, pekelný oheň, zmrzlý blesk, granátové jablko, ohnivá koule.").save()
    BeastWeakness(group='L',
                  note="4. skupina kouzel (fyzická) - améba, břichomluvectví, cizí oči, cizí uši, dlouhá ruka, hyperprostor, hyperprostor 2, mágův velký mix, Melenina krása, metamorfóza, metamorfóza 2, mrak smrti, neslyšitelnost, neviditelnost, nevycítitelnost, ochrom bleskem, orlí oči, plošný hyperprostor, procházení zdí, protoplazma, převtělení, přežij, rozptyl kouzla, rychlost, smrtící déšť, soví oči, vodní dech, všepronikání, zabij, zapůjčení, zažeň únavu, zesměšni, zlom kouzlo, zmiz, zpomalení.").save()
    BeastWeakness(group='M',
                  note="5. skupina kouzel (psychická) - čtení myšlenek, davová hypnóza, duševní rozštěp, hypnóza, kouzelná rušička, kouzlo spánku, Montyho čardáš, pamatuj, poslání, přežij, sugesce, svaž postavu, usni, vidění dvojmo, vzpomeň, zapomeň, zastrašení, Zenerova karta, zmatek, zmam osobu, čarovná mlha, hněv lesa, láska lesa, všechna psychická kouzla chodce.").save()
    BeastWeakness(group='N', note="6. skupina kouzel - bílá střela").save()
    BeastWeakness(group='O', note="Podrobování").save()
    BeastWeakness(group='P', note="Mentální útok").save()
    BeastWeakness(group='P+', note="Mentální útok (Příšera může sama mentální útok vyvolávat.").save()


# pylint: disable=unused-argument
def init_category(apps, schema_editor):
    """To init categories, just call this method in migration.
    Like this:
        migrations.RunPython(skill.init_category)
    Dont forget to import.
    """
    BeastCategory(name="Domorodci").save()
    BeastCategory(name="Draci").save()
    BeastCategory(name="Hmyz").save()
    BeastCategory(name="Humonoidi").save()
    BeastCategory(name="Lykantropové").save()
    BeastCategory(name="Magičtí tvorové").save()
    BeastCategory(name="Nemrtví").save()
    BeastCategory(name="Nevidění").save()
    BeastCategory(name="Okřídlení").save()
    BeastCategory(name="Plazi").save()
    BeastCategory(name="Šelmy").save()
    BeastCategory(name="Vodní tvorové").save()
    BeastCategory(name="Zvěř").save()


if settings.DEBUG:
    admin.site.register(BeastMobility)
    admin.site.register(BeastAttack)
    admin.site.register(BeastCategory)
    admin.site.register(BeastWeakness)

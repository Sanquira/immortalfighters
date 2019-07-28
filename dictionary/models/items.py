from django.db import models
from polymorphic.models import PolymorphicModel


class BaseItem(PolymorphicModel):
    name = models.CharField(max_length=100, null=False, default="Nový item", verbose_name="Předmět")
    note = models.TextField(null=True, verbose_name="Poznámka")
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, related_name="children",
                                 verbose_name="Kategorie")

    def __str__(self):
        return self.name


class Item(BaseItem):
    class Meta:
        verbose_name = "Předmět"
        verbose_name_plural = "Předměty"


class Artefact(BaseItem):
    mana = models.IntegerField(default=0, null=False, verbose_name="Mana")
    spells = models.ManyToManyField('Spell', verbose_name="Kouzla")

    class Meta:
        verbose_name = "Artefakt"
        verbose_name_plural = "Artefakty"

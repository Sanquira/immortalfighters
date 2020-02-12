"""Module for Item entity and corresponding objects."""
from django.db import models
from polymorphic.models import PolymorphicModel


class BaseItem(PolymorphicModel):
    """
    Model for base Item. Parent of all item types.
    """
    name = models.CharField(max_length=100, null=False, default="Nový item", verbose_name="Předmět")
    note = models.TextField(null=True, verbose_name="Poznámka")

    def __str__(self):
        return self.name


class Item(BaseItem):
    """
    Model for Item. Common item without any spells.
    """

    class Meta:
        verbose_name = "Předmět"
        verbose_name_plural = "Předměty"
        ordering = ['name']


class Artefact(BaseItem):
    """
    Model for Artefact. Special item containing Spells and mana.
    """
    mana = models.IntegerField(default=0, null=False, verbose_name="Mana")
    spells = models.ManyToManyField('Spell', verbose_name="Kouzla")

    class Meta:
        verbose_name = "Artefakt"
        verbose_name_plural = "Artefakty"

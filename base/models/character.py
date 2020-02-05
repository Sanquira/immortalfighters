"""Module for Character entity."""
from django.db import models

from base.models.ifuser import IFUser
from base.models.profession import BaseProfession
from base.models.race import Race


class Character(models.Model):
    """
    Model for Character.
    """
    owner = models.ForeignKey(IFUser, on_delete=models.CASCADE, verbose_name="Vlastník")
    character_name = models.CharField(max_length=50, null=True, verbose_name="Jméno postavy")
    race = models.ForeignKey(Race, on_delete=models.CASCADE, null=True, verbose_name="Rasa")
    profession = models.ForeignKey(BaseProfession, on_delete=models.CASCADE, null=True, verbose_name="Povolání")

    # stat_strength = models.PositiveSmallIntegerField(default=0)
    # stat_dexterity = models.PositiveSmallIntegerField(default=0)
    # stat_resistance = models.PositiveSmallIntegerField(default=0)
    # stat_intelligence = models.PositiveSmallIntegerField(default=0)
    # stat_charisma = models.PositiveSmallIntegerField(default=0)
    # experience_points = models.PositiveIntegerField(default=0)
    # level = models.PositiveSmallIntegerField(default=0)
    
    class Meta:
        verbose_name = "Postava"
        verbose_name_plural = "Postavy"

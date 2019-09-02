from django.db import models

from base.models import IFUser
from dictionary.models.profession import BaseProfession
from dictionary.models.race import Race


class Character(models.Model):
    owner = models.ForeignKey(IFUser, on_delete=models.CASCADE, verbose_name="Vlastník")
    character_name = models.CharField(max_length=50, null=True, verbose_name="Jméno postavy")
    race = models.ForeignKey(Race, on_delete=models.CASCADE, null=True, verbose_name="Rasa")
    profession = models.ForeignKey(BaseProfession, on_delete=models.CASCADE, null=True, verbose_name="Povolání")
    
    strength = models.PositiveSmallIntegerField(default=0, verbose_name="Síla")
    dexterity = models.PositiveSmallIntegerField(default=0, verbose_name="Obratnost")
    resistance = models.PositiveSmallIntegerField(default=0, verbose_name="Odolnost")
    intelligence = models.PositiveSmallIntegerField(default=0, verbose_name="Inteligence")
    charisma = models.PositiveSmallIntegerField(default=0, verbose_name="Charisma")
    experience_points = models.PositiveIntegerField(default=0, verbose_name="Zkušenosti")
    level = models.PositiveSmallIntegerField(default=0, verbose_name="Úroven")
    
    class Meta:
        verbose_name = "Postava"
        verbose_name_plural = "Postavy"

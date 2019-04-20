from django.db import models

from base.models import IFUser
from dictionary.models import Race, BaseProfession


class Character(models.Model):
    owner = models.ForeignKey(IFUser, on_delete=models.CASCADE)
    character_name = models.CharField(max_length=50, null=True)
    race = models.ForeignKey(Race, on_delete=models.CASCADE, null=True)
    profession = models.ForeignKey(BaseProfession, on_delete=models.CASCADE, null=True)

    stat_strength = models.PositiveSmallIntegerField(default=0)
    stat_dexterity = models.PositiveSmallIntegerField(default=0)
    stat_resistance = models.PositiveSmallIntegerField(default=0)
    stat_intelligence = models.PositiveSmallIntegerField(default=0)
    stat_charisma = models.PositiveSmallIntegerField(default=0)
    experience_points = models.PositiveIntegerField(default=0)
    level = models.PositiveSmallIntegerField(default=0)

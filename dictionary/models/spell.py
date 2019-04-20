from django.db import models

from dictionary.models.profession import BaseProfession


class Spell(models.Model):
    name = models.CharField(max_length=128, null=False, default="New spell")
    mana = models.CharField(max_length=128, null=True)
    range = models.CharField(max_length=32, null=True)
    cast_time = models.CharField(max_length=32, null=True)
    duration = models.CharField(max_length=32, null=True)
    note = models.TextField(null=True)

    available_for_professions = models.ManyToManyField(BaseProfession, through='ProfessionLimitation')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kouzlo"
        verbose_name_plural = "Kouzla"

from django.db import models

from dictionary.models.profession import BaseProfession


class Spell(models.Model):
    name = models.CharField(max_length=128, null=False, default="New spell",verbose_name="Jméno kouzla")
    mana = models.CharField(max_length=128, null=True,verbose_name="Mana")
    range = models.CharField(max_length=32, null=True,verbose_name="Dosah")
    cast_time = models.CharField(max_length=32, null=True,verbose_name="Vyvolání")
    duration = models.CharField(max_length=32, null=True,verbose_name="Trvání")
    note = models.TextField(null=True,verbose_name="Popis")

    available_for_professions = models.ManyToManyField(BaseProfession, through='ProfessionLimitation')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kouzlo"
        verbose_name_plural = "Kouzla"

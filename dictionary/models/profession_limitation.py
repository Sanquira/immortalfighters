from django.db import models

from dictionary.models.profession import BaseProfession


class ProfessionLimitation(models.Model):
    spell = models.ForeignKey('Spell', on_delete=models.CASCADE, verbose_name="Kouzlo")
    profession = models.ForeignKey(BaseProfession, on_delete=models.CASCADE,verbose_name="Povolání")
    from_level = models.PositiveSmallIntegerField(default=1,verbose_name="Od úrovně")

    def __str__(self):
        return self.profession.name + " - " + self.spell.name

    class Meta:
        verbose_name = "Povolání - kouzlo omezení"
        verbose_name_plural = verbose_name

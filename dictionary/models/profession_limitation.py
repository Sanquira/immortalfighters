from django.db import models

from dictionary.models.profession import BaseProfession


class ProfessionLimitation(models.Model):
    skill = models.ForeignKey('Spell', on_delete=models.CASCADE)
    profession = models.ForeignKey(BaseProfession, on_delete=models.CASCADE)
    from_level = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.profession.name + " - " + self.skill.name

    class Meta:
        verbose_name = "Povolání - kouzlo omezení"
        verbose_name_plural = verbose_name

from django.db import models

from dictionary.models import Spell
from dictionary.models.profession import BaseProfession


class ProfessionLimitation(models.Model):
    skill = models.ForeignKey(Spell, on_delete=models.CASCADE)
    profession = models.ForeignKey(BaseProfession, on_delete=models.CASCADE)
    from_level = models.PositiveSmallIntegerField(default=1)

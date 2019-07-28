from enum import Enum

from django.db import models
from markdownx.models import MarkdownxField

from base.models.stat import Stat


class SkillDifficulty(Enum):
    EASY = "Lehká"
    MEDIUM = "Střední"
    HARD = "Těžká"
    SUPER_HARD = "Velmi těžká"


# class SkillRank:
#     ranks = ("Vůbec", "Velmi špatně", "Špatně", "Průměrně", "Dobře", "Velmi dobře", "Dokonale")


class Skill(models.Model):
    name = models.CharField(max_length=128, null=False, default="Nová dovednost", verbose_name="Jméno dovednosti")
    stat = models.CharField(max_length=20, choices=[(tag.name, tag.value) for tag in Stat], verbose_name="Vlastnost")
    difficulty = models.CharField(max_length=20, choices=[(tag.name, tag.value) for tag in SkillDifficulty], verbose_name="Obtížnost")
    duration = models.CharField(max_length=128, null=True, verbose_name="Ověřování")
    success_total = MarkdownxField(null=True, verbose_name="Totální úspěch")
    success = MarkdownxField(null=True, verbose_name="Úspěch")
    failure = MarkdownxField(null=True, verbose_name="Neúspěch")
    failure_total = MarkdownxField(null=True, verbose_name="Totální neúspěch")
    note = MarkdownxField(null=True, verbose_name="Poznámka")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Dovednost"
        verbose_name_plural = "Dovednosti"

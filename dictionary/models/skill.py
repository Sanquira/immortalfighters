from enum import Enum

from django.db import models
from markdownx.models import MarkdownxField

from base.models.stat import Stat


class SkillDifficulty(Enum):
    EASY = "Lehká"
    MEDIUM = "Střední"
    HARD = "Těžká"
    EXTREME = "Velmi těžká"


class SkillRank(models.Model):
    name = models.CharField(max_length=20, verbose_name="Obtížnost")
    trap = models.SmallIntegerField(null=False, verbose_name="Past")
    
    def __str__(self):
        return self.name


class SkillPoints(models.Model):
    difficulty = models.CharField(max_length=20, choices=[(tag.name, tag.value) for tag in SkillDifficulty], verbose_name="Obtížnost")
    rank = models.ForeignKey(SkillRank, null=False, on_delete=models.CASCADE, verbose_name="Stupeň")
    points = models.SmallIntegerField(null=False, verbose_name="Body")
    
    def __str__(self):
        return self.difficulty + " - " + self.rank.__str__()
    
    class Meta:
        verbose_name = "Dovednostní body"
        verbose_name_plural = verbose_name


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


def init_skills(apps, schema_editor):
    """To init skills, just call this method in migration.
        Like this:
            migrations.RunPython(skill.init_skills)
        Dont forget to import.
        """
    
    D0 = SkillRank(name="Vůbec", trap=14)
    D1 = SkillRank(name="Velmi špatně", trap=11)
    D2 = SkillRank(name="Špatně", trap=8)
    D3 = SkillRank(name="Průměrně", trap=5)
    D4 = SkillRank(name="Dobře", trap=2)
    D5 = SkillRank(name="Velmi dobře", trap=-1)
    D6 = SkillRank(name="Dokonale", trap=-4)
    D0.save()
    D1.save()
    D2.save()
    D3.save()
    D4.save()
    D5.save()
    D6.save()
    
    SkillPoints(difficulty=SkillDifficulty.EASY.name, rank=D0, points=0).save()
    SkillPoints(difficulty=SkillDifficulty.EASY.name, rank=D1, points=3).save()
    SkillPoints(difficulty=SkillDifficulty.EASY.name, rank=D2, points=9).save()
    SkillPoints(difficulty=SkillDifficulty.EASY.name, rank=D3, points=18).save()
    SkillPoints(difficulty=SkillDifficulty.EASY.name, rank=D4, points=30).save()
    SkillPoints(difficulty=SkillDifficulty.EASY.name, rank=D5, points=45).save()
    SkillPoints(difficulty=SkillDifficulty.EASY.name, rank=D6, points=63).save()
    SkillPoints(difficulty=SkillDifficulty.MEDIUM.name, rank=D0, points=0).save()
    SkillPoints(difficulty=SkillDifficulty.MEDIUM.name, rank=D1, points=5).save()
    SkillPoints(difficulty=SkillDifficulty.MEDIUM.name, rank=D2, points=15).save()
    SkillPoints(difficulty=SkillDifficulty.MEDIUM.name, rank=D3, points=30).save()
    SkillPoints(difficulty=SkillDifficulty.MEDIUM.name, rank=D4, points=50).save()
    SkillPoints(difficulty=SkillDifficulty.MEDIUM.name, rank=D5, points=75).save()
    SkillPoints(difficulty=SkillDifficulty.MEDIUM.name, rank=D6, points=105).save()
    SkillPoints(difficulty=SkillDifficulty.HARD.name, rank=D0, points=0).save()
    SkillPoints(difficulty=SkillDifficulty.HARD.name, rank=D1, points=7).save()
    SkillPoints(difficulty=SkillDifficulty.HARD.name, rank=D2, points=21).save()
    SkillPoints(difficulty=SkillDifficulty.HARD.name, rank=D3, points=42).save()
    SkillPoints(difficulty=SkillDifficulty.HARD.name, rank=D4, points=70).save()
    SkillPoints(difficulty=SkillDifficulty.HARD.name, rank=D5, points=105).save()
    SkillPoints(difficulty=SkillDifficulty.HARD.name, rank=D6, points=147).save()
    SkillPoints(difficulty=SkillDifficulty.EXTREME.name, rank=D0, points=0).save()
    SkillPoints(difficulty=SkillDifficulty.EXTREME.name, rank=D1, points=9).save()
    SkillPoints(difficulty=SkillDifficulty.EXTREME.name, rank=D2, points=28).save()
    SkillPoints(difficulty=SkillDifficulty.EXTREME.name, rank=D3, points=54).save()
    SkillPoints(difficulty=SkillDifficulty.EXTREME.name, rank=D4, points=90).save()
    SkillPoints(difficulty=SkillDifficulty.EXTREME.name, rank=D5, points=130).save()
    SkillPoints(difficulty=SkillDifficulty.EXTREME.name, rank=D6, points=189).save()

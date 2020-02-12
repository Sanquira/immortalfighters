"""Module for Skill entity and corresponding objects."""
from django.conf import settings
from django.contrib import admin
from django.db import models
from markdownx.models import MarkdownxField

from base.models.stat import Stat


class SkillDifficulty(models.Model):
    """Model for Difficulty."""
    name = models.CharField(max_length=20, verbose_name="Obtížnost")

    def __str__(self):
        return self.name


class SkillRank(models.Model):
    """Model for Rank."""
    name = models.CharField(max_length=20, verbose_name="Stupeň")
    trap = models.SmallIntegerField(null=False, verbose_name="Past")

    def __str__(self):
        return self.name


class SkillPoints(models.Model):
    """Model for Point."""
    difficulty = models.ForeignKey(SkillDifficulty, on_delete=models.CASCADE, verbose_name="Obtížnost")
    rank = models.ForeignKey(SkillRank, null=False, on_delete=models.CASCADE, verbose_name="Stupeň")
    points = models.SmallIntegerField(null=False, verbose_name="Body")

    def __str__(self):
        return self.difficulty.name + " - " + self.rank.__str__()

    class Meta:
        verbose_name = "Dovednostní body"
        verbose_name_plural = verbose_name


class Skill(models.Model):
    """Model for Skill."""
    name = models.CharField(max_length=128, null=False, unique=True,
                            default="Nová dovednost", verbose_name="Jméno dovednosti")
    stat = models.ForeignKey(Stat, on_delete=models.CASCADE, verbose_name="Vlastnost")
    difficulty = models.ForeignKey(SkillDifficulty, on_delete=models.CASCADE, verbose_name="Obtížnost")
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
        ordering = ['name', 'stat']


# pylint: disable=unused-argument
def init_ranks_and_difficulty(apps, schema_editor):
    """To init skill ranks and diffs, just call this method in migration.
        Like this:
            migrations.RunPython(skill.init_ranks_and_difficulty)
        Dont forget to import.
        """
    SkillRank.objects.all().delete()
    SkillRank(name="Vůbec", trap=14).save()
    SkillRank(name="Velmi špatně", trap=11).save()
    SkillRank(name="Špatně", trap=8).save()
    SkillRank(name="Průměrně", trap=5).save()
    SkillRank(name="Dobře", trap=2).save()
    SkillRank(name="Velmi dobře", trap=-1).save()
    SkillRank(name="Dokonale", trap=-4).save()

    SkillDifficulty(name='Lehká').save()
    SkillDifficulty(name='Střední').save()
    SkillDifficulty(name='Těžká').save()
    SkillDifficulty(name='Velmi těžká').save()


# pylint: disable=unused-argument,invalid-name
def init_skills(apps, schema_editor):
    """To init skills, just call this method in migration.
        Like this:
            migrations.RunPython(skill.init_skills)
        Dont forget to import.
        """
    d0 = SkillDifficulty.objects.get(name="Lehká")
    d1 = SkillDifficulty.objects.get(name="Střední")
    d2 = SkillDifficulty.objects.get(name="Těžká")
    d3 = SkillDifficulty.objects.get(name="Velmi těžká")

    r0 = SkillRank.objects.get(trap=14)
    r1 = SkillRank.objects.get(trap=11)
    r2 = SkillRank.objects.get(trap=8)
    r3 = SkillRank.objects.get(trap=5)
    r4 = SkillRank.objects.get(trap=2)
    r5 = SkillRank.objects.get(trap=-1)
    r6 = SkillRank.objects.get(trap=-4)

    SkillPoints.objects.all().delete()
    SkillPoints(difficulty=d0, rank=r0, points=0).save()
    SkillPoints(difficulty=d0, rank=r1, points=3).save()
    SkillPoints(difficulty=d0, rank=r2, points=9).save()
    SkillPoints(difficulty=d0, rank=r3, points=18).save()
    SkillPoints(difficulty=d0, rank=r4, points=30).save()
    SkillPoints(difficulty=d0, rank=r5, points=45).save()
    SkillPoints(difficulty=d0, rank=r6, points=63).save()
    SkillPoints(difficulty=d1, rank=r0, points=0).save()
    SkillPoints(difficulty=d1, rank=r1, points=5).save()
    SkillPoints(difficulty=d1, rank=r2, points=15).save()
    SkillPoints(difficulty=d1, rank=r3, points=30).save()
    SkillPoints(difficulty=d1, rank=r4, points=50).save()
    SkillPoints(difficulty=d1, rank=r5, points=75).save()
    SkillPoints(difficulty=d1, rank=r6, points=105).save()
    SkillPoints(difficulty=d2, rank=r0, points=0).save()
    SkillPoints(difficulty=d2, rank=r1, points=7).save()
    SkillPoints(difficulty=d2, rank=r2, points=21).save()
    SkillPoints(difficulty=d2, rank=r3, points=42).save()
    SkillPoints(difficulty=d2, rank=r4, points=70).save()
    SkillPoints(difficulty=d2, rank=r5, points=105).save()
    SkillPoints(difficulty=d2, rank=r6, points=147).save()
    SkillPoints(difficulty=d3, rank=r0, points=0).save()
    SkillPoints(difficulty=d3, rank=r1, points=9).save()
    SkillPoints(difficulty=d3, rank=r2, points=28).save()
    SkillPoints(difficulty=d3, rank=r3, points=54).save()
    SkillPoints(difficulty=d3, rank=r4, points=90).save()
    SkillPoints(difficulty=d3, rank=r5, points=130).save()
    SkillPoints(difficulty=d3, rank=r6, points=189).save()


if settings.DEBUG:
    admin.site.register(SkillPoints)

from django.db import models


class Stat(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False, default="Jméno", verbose_name="Jméno statu")
    shortcut = models.CharField(max_length=3, null=False, blank=False, default="BLK", verbose_name="Zkratka statu")
    
    def __str__(self):
        return self.name


def init_stats(apps, schema_editor):
    """To init stats, just call this method in migration.
        Like this:
            migrations.RunPython(skill.init_stats)
        Dont forget to import.
        """
    Stat(name="Síla", shortcut="STR").save()
    Stat(name="Obratnost", shortcut="DEX").save()
    Stat(name="Odolnost", shortcut="RES").save()
    Stat(name="Inteligence", shortcut="INT").save()
    Stat(name="Charisma", shortcut="CHA").save()

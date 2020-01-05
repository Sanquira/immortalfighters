"""Module for CreatureSize entity and corresponding objects."""
from django.db import models


class CreatureSize(models.Model):
    """Model for CreatureSize."""
    name = models.CharField(max_length=8, null=False, unique=True, default='A', verbose_name="Velikost")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Velikostní třída"
        verbose_name_plural = "Velikostní třídy"


# pylint: disable=unused-argument
def init_creature_size(apps, schema_editor):
    """To init creature sizes, just call this method in migration.
        Like this:
            migrations.RunPython(skill.init_creature_size)
        Dont forget to import.
        """
    CreatureSize(name="A").save()
    CreatureSize(name="B").save()
    CreatureSize(name="C").save()
    CreatureSize(name="D").save()
    CreatureSize(name="E").save()

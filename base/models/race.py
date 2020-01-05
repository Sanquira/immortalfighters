"""Module for Race entity and corresponding objects."""
from django.db import models


# pylint: disable=too-many-instance-attributes
class Race(models.Model):
    """Model for Race."""
    name = models.CharField(max_length=50, null=False, default="Název rasy", verbose_name="Název rasy")
    str_min = models.SmallIntegerField(default=0, verbose_name="Síla minimum")
    str_max = models.SmallIntegerField(default=0, verbose_name="Síla maximum")
    str_fix = models.SmallIntegerField(default=0, verbose_name="Síla oprava")
    dex_min = models.SmallIntegerField(default=0, verbose_name="Obratnost minimum")
    dex_max = models.SmallIntegerField(default=0, verbose_name="Obratnost maximum")
    dex_fix = models.SmallIntegerField(default=0, verbose_name="Obratnost oprava")
    res_min = models.SmallIntegerField(default=0, verbose_name="Odolnost minimum")
    res_max = models.SmallIntegerField(default=0, verbose_name="Odolnost maximum")
    res_fix = models.SmallIntegerField(default=0, verbose_name="Odolnost oprava")
    int_min = models.SmallIntegerField(default=0, verbose_name="Inteligence minimum")
    int_max = models.SmallIntegerField(default=0, verbose_name="Inteligence maximum")
    int_fix = models.SmallIntegerField(default=0, verbose_name="Inteligence oprava")
    cha_min = models.SmallIntegerField(default=0, verbose_name="Charisma minimum")
    cha_max = models.SmallIntegerField(default=0, verbose_name="Charisma maximum")
    cha_fix = models.SmallIntegerField(default=0, verbose_name="Charisma oprava")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Rasa"
        verbose_name_plural = "Rasy"
    
    # pylint: disable=too-many-locals, too-many-arguments
    def race_factory(self, name: str, str_min: int, str_max: int, dex_min: int, dex_max: int, res_min: int,
                     res_max: int, int_min: int, int_max: int, cha_min: int, cha_max: int, str_fix: int, dex_fix: int,
                     res_fix: int, int_fix: int, cha_fix: int):
        """Factory for Race."""
        self.name = name
        self.str_min = str_min
        self.str_max = str_max
        self.str_fix = str_fix
        self.dex_min = dex_min
        self.dex_max = dex_max
        self.dex_fix = dex_fix
        self.res_min = res_min
        self.res_max = res_max
        self.res_fix = res_fix
        self.int_min = int_min
        self.int_max = int_max
        self.int_fix = int_fix
        self.cha_min = cha_min
        self.cha_max = cha_max
        self.cha_fix = cha_fix


# pylint: disable=unused-argument
def initialize_races(apps, schema_editor):
    """To init races, just call this method in migration.
    Like this:
        migrations.RunPython(race.initialize_races)
    Dont forget to import.
    """
    hobit = Race()
    hobit.race_factory("Hobit", 3, 8, 11, 16, 8, 13, 10, 15, 8, 18, -5, 2, 0, -2, +3)
    kuduk = Race()
    kuduk.race_factory("Kudůk", 5, 10, 10, 15, 10, 15, 9, 14, 7, 12, -3, 1, 1, -2, 0)
    trpaslik = Race()
    trpaslik.race_factory("Trpaslík", 7, 12, 7, 12, 12, 17, 8, 13, 7, 12, 1, -2, 3, -3, -2)
    elf = Race()
    elf.race_factory("Elf", 6, 11, 10, 15, 6, 11, 12, 17, 8, 18, 0, 1, -4, 2, 2)
    clovek = Race()
    clovek.race_factory("Člověk", 6, 16, 9, 14, 9, 14, 10, 15, 2, 17, 0, 0, 0, 0, 0)
    barbar = Race()
    barbar.race_factory("Barbar", 10, 15, 8, 13, 11, 16, 6, 11, 1, 16, 1, -1, 1, 0, -2)
    kroll = Race()
    kroll.race_factory("Kroll", 11, 16, 5, 10, 13, 18, 2, 7, 1, 11, 3, -4, 3, -6, -5)
    hobit.save()
    kuduk.save()
    trpaslik.save()
    elf.save()
    clovek.save()
    barbar.save()
    kroll.save()

from django.db import models
from polymorphic.models import PolymorphicModel


class BaseProfession(PolymorphicModel):
    name = models.CharField(max_length=50, null=False, default="Název povolání", verbose_name="Název povolání")
    parentProf = models.ForeignKey('BaseProfession', on_delete=models.CASCADE, null=True, blank=True)
    str_min = models.SmallIntegerField(default=0, verbose_name="Síla minimum")
    str_max = models.SmallIntegerField(default=0, verbose_name="Síla maximum")
    dex_min = models.SmallIntegerField(default=0, verbose_name="Obratnost minimum")
    dex_max = models.SmallIntegerField(default=0, verbose_name="Obratnost maximum")
    res_min = models.SmallIntegerField(default=0, verbose_name="Odolnost minimum")
    res_max = models.SmallIntegerField(default=0, verbose_name="Odolnost maximum")
    int_min = models.SmallIntegerField(default=0, verbose_name="Inteligence minimum")
    int_max = models.SmallIntegerField(default=0, verbose_name="Inteligence maximum")
    cha_min = models.SmallIntegerField(default=0, verbose_name="Charisma minimum")
    cha_max = models.SmallIntegerField(default=0, verbose_name="Charisma maximum")
    hp_start = models.SmallIntegerField(default=0, verbose_name="Počáteční životy")
    hp_dice = models.SmallIntegerField(default=0, verbose_name="Kostka na životy")
    hp_dice_fix = models.SmallIntegerField(default=0, verbose_name="Oprava kostky na životy")
    hp_9 = models.SmallIntegerField(default=0, verbose_name="Životy od 9 úrovně")

    # def get_level_from_xp(self, xp: int) -> int:
    #     pass
    #
    # def get_level_xp(self, level: int) -> int:
    #     pass
    #
    # def get_level_price(self, level: int) -> int:
    #     pass

    def get_hp(self) -> int:
        return self.hp_start

    def get_hp_dice(self) -> int:
        return self.hp_dice

    def get_dice_fix(self) -> int:
        return self.hp_dice_fix

    def get_hp_9(self) -> int:
        return self.hp_9

    def profession_factory(self, name: str, parent_prof: 'BaseProfession', str_min=0, str_max=0, dex_min=0, dex_max=0,
                           res_min=0, res_max=0, int_min=0, int_max=0, cha_min=0, cha_max=0, hp_start=0, hp_dice=0,
                           hp_dice_fix=0, hp_9=0):
        self.name = name
        if parent_prof is not None:
            self.parentProf = parent_prof
            self.str_min = parent_prof.str_min
            self.str_max = parent_prof.str_max
            self.dex_min = parent_prof.dex_min
            self.dex_max = parent_prof.dex_max
            self.res_min = parent_prof.res_min
            self.res_max = parent_prof.res_max
            self.int_min = parent_prof.int_min
            self.int_max = parent_prof.int_max
            self.cha_min = parent_prof.cha_min
            self.cha_max = parent_prof.cha_max
            self.hp_start = parent_prof.hp_start
            self.hp_dice = parent_prof.hp_dice
            self.hp_dice_fix = parent_prof.hp_dice_fix
            self.hp_9 = parent_prof.hp_9
        else:
            self.str_min = str_min
            self.str_max = str_max
            self.dex_min = dex_min
            self.dex_max = dex_max
            self.res_min = res_min
            self.res_max = res_max
            self.int_min = int_min
            self.int_max = int_max
            self.cha_min = cha_min
            self.cha_max = cha_max
            self.hp_start = hp_start
            self.hp_dice = hp_dice
            self.hp_dice_fix = hp_dice_fix
            self.hp_9 = hp_9

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Povolání"
        verbose_name_plural = verbose_name


class XPLevel(models.Model):
    profession = models.ForeignKey(BaseProfession, on_delete=models.CASCADE)
    level = models.SmallIntegerField(default=0, verbose_name="Úroveň")
    xp_needed = models.IntegerField(default=0, verbose_name="Zkušenosti")
    money_needed = models.IntegerField(default=0, verbose_name="Cena")

    def xp_level_factory(self, prof: BaseProfession, level: int, xp: int, money: int):
        self.profession = prof
        self.level = level
        self.xp_needed = xp
        self.money_needed = money

    def __str__(self):
        return self.profession.name + "_" + str(self.level)

    class Meta:
        verbose_name = "Úroveň"
        verbose_name_plural = "Úrovně"


class MagicUser(models.Model):

    def get_mana(self):
        pass

    class Meta:
        abstract = True


def init_professions(apps, schema_editor):
    """To init professions, just call this method in migration.
        Like this:
            migrations.RunPython(profession.init_professions)
        Dont forget to import.
        """
    alchemist = BaseProfession()
    alchemist.profession_factory("Alchymista", None, 13, 18, 0, 0, 13, 18, 0, 0, 0, 0, 10, 10, 0, 2)
    ranger = BaseProfession()
    ranger.profession_factory("Hraničář", None, 11, 16, 0, 0, 0, 0, 12, 17, 0, 0, 8, 6, 2, 2)
    wizard = BaseProfession()
    wizard.profession_factory("Kouzelník", None, 0, 0, 13, 18, 12, 17, 0, 0, 0, 0, 7, 6, 1, 1)
    warrior = BaseProfession()
    warrior.profession_factory("Válečník", None, 0, 0, 0, 0, 0, 0, 14, 19, 13, 18, 6, 6, 0, 1)
    thief = BaseProfession()
    thief.profession_factory("Zloděj", None, 0, 0, 14, 19, 0, 0, 0, 0, 12, 17, 6, 6, 0, 1)
    alchemist.save()
    ranger.save()
    wizard.save()
    warrior.save()
    thief.save()
    theurg = BaseProfession()
    theurg.profession_factory("Theurg", alchemist)
    pyrofor = BaseProfession()
    pyrofor.profession_factory("Pyrofor", alchemist)
    druid = BaseProfession()
    druid.profession_factory("Druid", ranger)
    walker = BaseProfession()
    walker.profession_factory("Chodec", ranger)
    caster = BaseProfession()
    caster.profession_factory("Kouzelník", wizard)
    mage = BaseProfession()
    mage.profession_factory("Mág", wizard)
    swordsman = BaseProfession()
    swordsman.profession_factory("Šermíř", warrior)
    fighter = BaseProfession()
    fighter.profession_factory("Bojovník", warrior)
    thug = BaseProfession()
    thug.profession_factory("Lupič", thief)
    sicco = BaseProfession()
    sicco.profession_factory("Sicco", thief)
    theurg.save()
    pyrofor.save()
    druid.save()
    walker.save()
    caster.save()
    mage.save()
    swordsman.save()
    fighter.save()
    thug.save()
    sicco.save()

    xp_level_warrior_2 = XPLevel()
    xp_level_warrior_2.xp_level_factory(warrior, 2, 450, 2)
    xp_level_warrior_2.save()
    xp_level_warrior_3 = XPLevel()
    xp_level_warrior_3.xp_level_factory(warrior, 3, 900, 4)
    xp_level_warrior_3.save()
    xp_level_warrior_4 = XPLevel()
    xp_level_warrior_4.xp_level_factory(warrior, 4, 1825, 8)
    xp_level_warrior_4.save()
    xp_level_warrior_5 = XPLevel()
    xp_level_warrior_5.xp_level_factory(warrior, 5, 3675, 13)
    xp_level_warrior_5.save()
    xp_level_warrior_6 = XPLevel()
    xp_level_warrior_6.xp_level_factory(warrior, 6, 7400, 19)
    xp_level_warrior_6.save()
    xp_level_warrior_7 = XPLevel()
    xp_level_warrior_7.xp_level_factory(warrior, 7, 15000, 26)
    xp_level_warrior_7.save()
    xp_level_warrior_8 = XPLevel()
    xp_level_warrior_8.xp_level_factory(warrior, 8, 30000, 34)
    xp_level_warrior_8.save()
    xp_level_warrior_9 = XPLevel()
    xp_level_warrior_9.xp_level_factory(warrior, 9, 55000, 43)
    xp_level_warrior_9.save()
    xp_level_warrior_10 = XPLevel()
    xp_level_warrior_10.xp_level_factory(warrior, 10, 83000, 53)
    xp_level_warrior_10.save()
    xp_level_warrior_11 = XPLevel()
    xp_level_warrior_11.xp_level_factory(warrior, 11, 114000, 64)
    xp_level_warrior_11.save()
    xp_level_warrior_12 = XPLevel()
    xp_level_warrior_12.xp_level_factory(warrior, 12, 148000, 77)
    xp_level_warrior_12.save()
    xp_level_warrior_13 = XPLevel()
    xp_level_warrior_13.xp_level_factory(warrior, 13, 185000, 90)
    xp_level_warrior_13.save()
    xp_level_warrior_14 = XPLevel()
    xp_level_warrior_14.xp_level_factory(warrior, 14, 225000, 105)
    xp_level_warrior_14.save()
    xp_level_warrior_15 = XPLevel()
    xp_level_warrior_15.xp_level_factory(warrior, 15, 273000, 120)
    xp_level_warrior_15.save()
    xp_level_warrior_16 = XPLevel()
    xp_level_warrior_16.xp_level_factory(warrior, 16, 324000, 137)
    xp_level_warrior_16.save()
    xp_level_warrior_17 = XPLevel()
    xp_level_warrior_17.xp_level_factory(warrior, 17, 362000, 155)
    xp_level_warrior_17.save()
    xp_level_warrior_18 = XPLevel()
    xp_level_warrior_18.xp_level_factory(warrior, 18, 412000, 173)
    xp_level_warrior_18.save()
    xp_level_warrior_19 = XPLevel()
    xp_level_warrior_19.xp_level_factory(warrior, 19, 464000, 193)
    xp_level_warrior_19.save()
    xp_level_warrior_20 = XPLevel()
    xp_level_warrior_20.xp_level_factory(warrior, 20, 518000, 214)
    xp_level_warrior_20.save()
    xp_level_warrior_21 = XPLevel()
    xp_level_warrior_21.xp_level_factory(warrior, 21, 574000, 237)
    xp_level_warrior_21.save()
    xp_level_warrior_22 = XPLevel()
    xp_level_warrior_22.xp_level_factory(warrior, 22, 632000, 260)
    xp_level_warrior_22.save()
    xp_level_warrior_23 = XPLevel()
    xp_level_warrior_23.xp_level_factory(warrior, 23, 692000, 284)
    xp_level_warrior_23.save()
    xp_level_warrior_24 = XPLevel()
    xp_level_warrior_24.xp_level_factory(warrior, 24, 754000, 309)
    xp_level_warrior_24.save()
    xp_level_warrior_25 = XPLevel()
    xp_level_warrior_25.xp_level_factory(warrior, 25, 818000, 336)
    xp_level_warrior_25.save()
    xp_level_warrior_26 = XPLevel()
    xp_level_warrior_26.xp_level_factory(warrior, 26, 884000, 363)
    xp_level_warrior_26.save()
    xp_level_warrior_27 = XPLevel()
    xp_level_warrior_27.xp_level_factory(warrior, 27, 951000, 392)
    xp_level_warrior_27.save()
    xp_level_warrior_28 = XPLevel()
    xp_level_warrior_28.xp_level_factory(warrior, 28, 1019000, 422)
    xp_level_warrior_28.save()
    xp_level_warrior_29 = XPLevel()
    xp_level_warrior_29.xp_level_factory(warrior, 29, 1088000, 452)
    xp_level_warrior_29.save()
    xp_level_warrior_30 = XPLevel()
    xp_level_warrior_30.xp_level_factory(warrior, 30, 1158000, 484)
    xp_level_warrior_30.save()
    xp_level_warrior_31 = XPLevel()
    xp_level_warrior_31.xp_level_factory(warrior, 31, 1229000, 517)
    xp_level_warrior_31.save()
    xp_level_warrior_32 = XPLevel()
    xp_level_warrior_32.xp_level_factory(warrior, 32, 1301000, 551)
    xp_level_warrior_32.save()
    xp_level_warrior_33 = XPLevel()
    xp_level_warrior_33.xp_level_factory(warrior, 33, 1374000, 586)
    xp_level_warrior_33.save()
    xp_level_warrior_34 = XPLevel()
    xp_level_warrior_34.xp_level_factory(warrior, 34, 1448000, 622)
    xp_level_warrior_34.save()
    xp_level_warrior_35 = XPLevel()
    xp_level_warrior_35.xp_level_factory(warrior, 35, 1523000, 660)
    xp_level_warrior_35.save()
    xp_level_warrior_36 = XPLevel()
    xp_level_warrior_36.xp_level_factory(warrior, 36, 1599000, 698)
    xp_level_warrior_36.save()

    xp_level_ranger_2 = XPLevel()
    xp_level_ranger_2.xp_level_factory(ranger, 2, 525, 2)
    xp_level_ranger_2.save()
    xp_level_ranger_3 = XPLevel()
    xp_level_ranger_3.xp_level_factory(ranger, 3, 1050, 4)
    xp_level_ranger_3.save()
    xp_level_ranger_4 = XPLevel()
    xp_level_ranger_4.xp_level_factory(ranger, 4, 2075, 8)
    xp_level_ranger_4.save()
    xp_level_ranger_5 = XPLevel()
    xp_level_ranger_5.xp_level_factory(ranger, 5, 4125, 13)
    xp_level_ranger_5.save()
    xp_level_ranger_6 = XPLevel()
    xp_level_ranger_6.xp_level_factory(ranger, 6, 8225, 19)
    xp_level_ranger_6.save()
    xp_level_ranger_7 = XPLevel()
    xp_level_ranger_7.xp_level_factory(ranger, 7, 16350, 26)
    xp_level_ranger_7.save()
    xp_level_ranger_8 = XPLevel()
    xp_level_ranger_8.xp_level_factory(ranger, 8, 32500, 34)
    xp_level_ranger_8.save()
    xp_level_ranger_9 = XPLevel()
    xp_level_ranger_9.xp_level_factory(ranger, 9, 57500, 44)
    xp_level_ranger_9.save()
    xp_level_ranger_10 = XPLevel()
    xp_level_ranger_10.xp_level_factory(ranger, 10, 85500, 54)
    xp_level_ranger_10.save()
    xp_level_ranger_11 = XPLevel()
    xp_level_ranger_11.xp_level_factory(ranger, 11, 116500, 66)
    xp_level_ranger_11.save()
    xp_level_ranger_12 = XPLevel()
    xp_level_ranger_12.xp_level_factory(ranger, 12, 150500, 78)
    xp_level_ranger_12.save()
    xp_level_ranger_13 = XPLevel()
    xp_level_ranger_13.xp_level_factory(ranger, 13, 187500, 92)
    xp_level_ranger_13.save()
    xp_level_ranger_14 = XPLevel()
    xp_level_ranger_14.xp_level_factory(ranger, 14, 227500, 107)
    xp_level_ranger_14.save()
    xp_level_ranger_15 = XPLevel()
    xp_level_ranger_15.xp_level_factory(ranger, 15, 257500, 123)
    xp_level_ranger_15.save()
    xp_level_ranger_16 = XPLevel()
    xp_level_ranger_16.xp_level_factory(ranger, 16, 326500, 140)
    xp_level_ranger_16.save()
    xp_level_ranger_17 = XPLevel()
    xp_level_ranger_17.xp_level_factory(ranger, 17, 364500, 159)
    xp_level_ranger_17.save()
    xp_level_ranger_18 = XPLevel()
    xp_level_ranger_18.xp_level_factory(ranger, 18, 414500, 178)
    xp_level_ranger_18.save()
    xp_level_ranger_19 = XPLevel()
    xp_level_ranger_19.xp_level_factory(ranger, 19, 466500, 199)
    xp_level_ranger_19.save()
    xp_level_ranger_20 = XPLevel()
    xp_level_ranger_20.xp_level_factory(ranger, 20, 520500, 220)
    xp_level_ranger_20.save()
    xp_level_ranger_21 = XPLevel()
    xp_level_ranger_21.xp_level_factory(ranger, 21, 576500, 243)
    xp_level_ranger_21.save()
    xp_level_ranger_22 = XPLevel()
    xp_level_ranger_22.xp_level_factory(ranger, 22, 634500, 267)
    xp_level_ranger_22.save()
    xp_level_ranger_23 = XPLevel()
    xp_level_ranger_23.xp_level_factory(ranger, 23, 694500, 292)
    xp_level_ranger_23.save()
    xp_level_ranger_24 = XPLevel()
    xp_level_ranger_24.xp_level_factory(ranger, 24, 756500, 318)
    xp_level_ranger_24.save()
    xp_level_ranger_25 = XPLevel()
    xp_level_ranger_25.xp_level_factory(ranger, 25, 820500, 345)
    xp_level_ranger_25.save()
    xp_level_ranger_26 = XPLevel()
    xp_level_ranger_26.xp_level_factory(ranger, 26, 886500, 373)
    xp_level_ranger_26.save()
    xp_level_ranger_27 = XPLevel()
    xp_level_ranger_27.xp_level_factory(ranger, 27, 953500, 403)
    xp_level_ranger_27.save()
    xp_level_ranger_28 = XPLevel()
    xp_level_ranger_28.xp_level_factory(ranger, 28, 1021500, 433)
    xp_level_ranger_28.save()
    xp_level_ranger_29 = XPLevel()
    xp_level_ranger_29.xp_level_factory(ranger, 29, 1090500, 465)
    xp_level_ranger_29.save()
    xp_level_ranger_30 = XPLevel()
    xp_level_ranger_30.xp_level_factory(ranger, 30, 1160500, 498)
    xp_level_ranger_30.save()
    xp_level_ranger_31 = XPLevel()
    xp_level_ranger_31.xp_level_factory(ranger, 31, 1231500, 532)
    xp_level_ranger_31.save()
    xp_level_ranger_32 = XPLevel()
    xp_level_ranger_32.xp_level_factory(ranger, 32, 1303500, 567)
    xp_level_ranger_32.save()
    xp_level_ranger_33 = XPLevel()
    xp_level_ranger_33.xp_level_factory(ranger, 33, 1376500, 603)
    xp_level_ranger_33.save()
    xp_level_ranger_34 = XPLevel()
    xp_level_ranger_34.xp_level_factory(ranger, 34, 1450500, 610)
    xp_level_ranger_34.save()
    xp_level_ranger_35 = XPLevel()
    xp_level_ranger_35.xp_level_factory(ranger, 35, 1525500, 678)
    xp_level_ranger_35.save()
    xp_level_ranger_36 = XPLevel()
    xp_level_ranger_36.xp_level_factory(ranger, 36, 1601500, 718)
    xp_level_ranger_36.save()

    xp_level_alchemist_2 = XPLevel()
    xp_level_alchemist_2.xp_level_factory(alchemist, 2, 575, 2)
    xp_level_alchemist_2.save()
    xp_level_alchemist_3 = XPLevel()
    xp_level_alchemist_3.xp_level_factory(alchemist, 3, 1150, 4)
    xp_level_alchemist_3.save()
    xp_level_alchemist_4 = XPLevel()
    xp_level_alchemist_4.xp_level_factory(alchemist, 4, 2300, 8)
    xp_level_alchemist_4.save()
    xp_level_alchemist_5 = XPLevel()
    xp_level_alchemist_5.xp_level_factory(alchemist, 5, 4650, 13)
    xp_level_alchemist_5.save()
    xp_level_alchemist_6 = XPLevel()
    xp_level_alchemist_6.xp_level_factory(alchemist, 6, 9325, 19)
    xp_level_alchemist_6.save()
    xp_level_alchemist_7 = XPLevel()
    xp_level_alchemist_7.xp_level_factory(alchemist, 7, 18700, 26)
    xp_level_alchemist_7.save()
    xp_level_alchemist_8 = XPLevel()
    xp_level_alchemist_8.xp_level_factory(alchemist, 8, 37500, 35)
    xp_level_alchemist_8.save()
    xp_level_alchemist_9 = XPLevel()
    xp_level_alchemist_9.xp_level_factory(alchemist, 9, 62500, 44)
    xp_level_alchemist_9.save()
    xp_level_alchemist_10 = XPLevel()
    xp_level_alchemist_10.xp_level_factory(alchemist, 10, 90500, 55)
    xp_level_alchemist_10.save()
    xp_level_alchemist_11 = XPLevel()
    xp_level_alchemist_11.xp_level_factory(alchemist, 11, 121500, 67)
    xp_level_alchemist_11.save()
    xp_level_alchemist_12 = XPLevel()
    xp_level_alchemist_12.xp_level_factory(alchemist, 12, 155500, 79)
    xp_level_alchemist_12.save()
    xp_level_alchemist_13 = XPLevel()
    xp_level_alchemist_13.xp_level_factory(alchemist, 13, 192500, 94)
    xp_level_alchemist_13.save()
    xp_level_alchemist_14 = XPLevel()
    xp_level_alchemist_14.xp_level_factory(alchemist, 14, 232500, 109)
    xp_level_alchemist_14.save()
    xp_level_alchemist_15 = XPLevel()
    xp_level_alchemist_15.xp_level_factory(alchemist, 15, 280500, 125)
    xp_level_alchemist_15.save()
    xp_level_alchemist_16 = XPLevel()
    xp_level_alchemist_16.xp_level_factory(alchemist, 16, 331500, 142)
    xp_level_alchemist_16.save()
    xp_level_alchemist_17 = XPLevel()
    xp_level_alchemist_17.xp_level_factory(alchemist, 17, 369500, 161)
    xp_level_alchemist_17.save()
    xp_level_alchemist_18 = XPLevel()
    xp_level_alchemist_18.xp_level_factory(alchemist, 18, 419500, 181)
    xp_level_alchemist_18.save()
    xp_level_alchemist_19 = XPLevel()
    xp_level_alchemist_19.xp_level_factory(alchemist, 19, 471500, 201)
    xp_level_alchemist_19.save()
    xp_level_alchemist_20 = XPLevel()
    xp_level_alchemist_20.xp_level_factory(alchemist, 20, 525500, 223)
    xp_level_alchemist_20.save()
    xp_level_alchemist_21 = XPLevel()
    xp_level_alchemist_21.xp_level_factory(alchemist, 21, 581500, 246)
    xp_level_alchemist_21.save()
    xp_level_alchemist_22 = XPLevel()
    xp_level_alchemist_22.xp_level_factory(alchemist, 22, 639500, 271)
    xp_level_alchemist_22.save()
    xp_level_alchemist_23 = XPLevel()
    xp_level_alchemist_23.xp_level_factory(alchemist, 23, 699500, 296)
    xp_level_alchemist_23.save()
    xp_level_alchemist_24 = XPLevel()
    xp_level_alchemist_24.xp_level_factory(alchemist, 24, 761500, 322)
    xp_level_alchemist_24.save()
    xp_level_alchemist_25 = XPLevel()
    xp_level_alchemist_25.xp_level_factory(alchemist, 25, 825500, 350)
    xp_level_alchemist_25.save()
    xp_level_alchemist_26 = XPLevel()
    xp_level_alchemist_26.xp_level_factory(alchemist, 26, 891500, 379)
    xp_level_alchemist_26.save()
    xp_level_alchemist_27 = XPLevel()
    xp_level_alchemist_27.xp_level_factory(alchemist, 27, 958500, 409)
    xp_level_alchemist_27.save()
    xp_level_alchemist_28 = XPLevel()
    xp_level_alchemist_28.xp_level_factory(alchemist, 28, 1026500, 440)
    xp_level_alchemist_28.save()
    xp_level_alchemist_29 = XPLevel()
    xp_level_alchemist_29.xp_level_factory(alchemist, 29, 1095500, 472)
    xp_level_alchemist_29.save()
    xp_level_alchemist_30 = XPLevel()
    xp_level_alchemist_30.xp_level_factory(alchemist, 30, 1165500, 505)
    xp_level_alchemist_30.save()
    xp_level_alchemist_31 = XPLevel()
    xp_level_alchemist_31.xp_level_factory(alchemist, 31, 1236500, 539)
    xp_level_alchemist_31.save()
    xp_level_alchemist_32 = XPLevel()
    xp_level_alchemist_32.xp_level_factory(alchemist, 32, 1308500, 575)
    xp_level_alchemist_32.save()
    xp_level_alchemist_33 = XPLevel()
    xp_level_alchemist_33.xp_level_factory(alchemist, 33, 1381500, 611)
    xp_level_alchemist_33.save()
    xp_level_alchemist_34 = XPLevel()
    xp_level_alchemist_34.xp_level_factory(alchemist, 34, 1455500, 649)
    xp_level_alchemist_34.save()
    xp_level_alchemist_35 = XPLevel()
    xp_level_alchemist_35.xp_level_factory(alchemist, 35, 1530500, 688)
    xp_level_alchemist_35.save()
    xp_level_alchemist_36 = XPLevel()
    xp_level_alchemist_36.xp_level_factory(alchemist, 36, 1606500, 728)
    xp_level_alchemist_36.save()

    xp_level_wizard_2 = XPLevel()
    xp_level_wizard_2.xp_level_factory(wizard, 2, 610, 2)
    xp_level_wizard_2.save()
    xp_level_wizard_3 = XPLevel()
    xp_level_wizard_3.xp_level_factory(wizard, 3, 1250, 4)
    xp_level_wizard_3.save()
    xp_level_wizard_4 = XPLevel()
    xp_level_wizard_4.xp_level_factory(wizard, 4, 2575, 8)
    xp_level_wizard_4.save()
    xp_level_wizard_5 = XPLevel()
    xp_level_wizard_5.xp_level_factory(wizard, 5, 5250, 13)
    xp_level_wizard_5.save()
    xp_level_wizard_6 = XPLevel()
    xp_level_wizard_6.xp_level_factory(wizard, 6, 10750, 19)
    xp_level_wizard_6.save()
    xp_level_wizard_7 = XPLevel()
    xp_level_wizard_7.xp_level_factory(wizard, 7, 22000, 26)
    xp_level_wizard_7.save()
    xp_level_wizard_8 = XPLevel()
    xp_level_wizard_8.xp_level_factory(wizard, 8, 37500, 35)
    xp_level_wizard_8.save()
    xp_level_wizard_9 = XPLevel()
    xp_level_wizard_9.xp_level_factory(wizard, 9, 62500, 44)
    xp_level_wizard_9.save()
    xp_level_wizard_10 = XPLevel()
    xp_level_wizard_10.xp_level_factory(wizard, 10, 90500, 55)
    xp_level_wizard_10.save()
    xp_level_wizard_11 = XPLevel()
    xp_level_wizard_11.xp_level_factory(wizard, 11, 121500, 67)
    xp_level_wizard_11.save()
    xp_level_wizard_12 = XPLevel()
    xp_level_wizard_12.xp_level_factory(wizard, 12, 155500, 79)
    xp_level_wizard_12.save()
    xp_level_wizard_13 = XPLevel()
    xp_level_wizard_13.xp_level_factory(wizard, 13, 192500, 94)
    xp_level_wizard_13.save()
    xp_level_wizard_14 = XPLevel()
    xp_level_wizard_14.xp_level_factory(wizard, 14, 232500, 109)
    xp_level_wizard_14.save()
    xp_level_wizard_15 = XPLevel()
    xp_level_wizard_15.xp_level_factory(wizard, 15, 280500, 125)
    xp_level_wizard_15.save()
    xp_level_wizard_16 = XPLevel()
    xp_level_wizard_16.xp_level_factory(wizard, 16, 331500, 142)
    xp_level_wizard_16.save()
    xp_level_wizard_17 = XPLevel()
    xp_level_wizard_17.xp_level_factory(wizard, 17, 377000, 162)
    xp_level_wizard_17.save()
    xp_level_wizard_18 = XPLevel()
    xp_level_wizard_18.xp_level_factory(wizard, 18, 427000, 182)
    xp_level_wizard_18.save()
    xp_level_wizard_19 = XPLevel()
    xp_level_wizard_19.xp_level_factory(wizard, 19, 479000, 203)
    xp_level_wizard_19.save()
    xp_level_wizard_20 = XPLevel()
    xp_level_wizard_20.xp_level_factory(wizard, 20, 533000, 225)
    xp_level_wizard_20.save()
    xp_level_wizard_21 = XPLevel()
    xp_level_wizard_21.xp_level_factory(wizard, 21, 589000, 249)
    xp_level_wizard_21.save()
    xp_level_wizard_22 = XPLevel()
    xp_level_wizard_22.xp_level_factory(wizard, 22, 647000, 273)
    xp_level_wizard_22.save()
    xp_level_wizard_23 = XPLevel()
    xp_level_wizard_23.xp_level_factory(wizard, 23, 707000, 298)
    xp_level_wizard_23.save()
    xp_level_wizard_24 = XPLevel()
    xp_level_wizard_24.xp_level_factory(wizard, 24, 769000, 325)
    xp_level_wizard_24.save()
    xp_level_wizard_25 = XPLevel()
    xp_level_wizard_25.xp_level_factory(wizard, 25, 843000, 353)
    xp_level_wizard_25.save()
    xp_level_wizard_26 = XPLevel()
    xp_level_wizard_26.xp_level_factory(wizard, 26, 899000, 382)
    xp_level_wizard_26.save()
    xp_level_wizard_27 = XPLevel()
    xp_level_wizard_27.xp_level_factory(wizard, 27, 966000, 412)
    xp_level_wizard_27.save()
    xp_level_wizard_28 = XPLevel()
    xp_level_wizard_28.xp_level_factory(wizard, 28, 1034000, 443)
    xp_level_wizard_28.save()
    xp_level_wizard_29 = XPLevel()
    xp_level_wizard_29.xp_level_factory(wizard, 29, 1103000, 476)
    xp_level_wizard_29.save()
    xp_level_wizard_30 = XPLevel()
    xp_level_wizard_30.xp_level_factory(wizard, 30, 1173000, 509)
    xp_level_wizard_30.save()
    xp_level_wizard_31 = XPLevel()
    xp_level_wizard_31.xp_level_factory(wizard, 31, 1244000, 544)
    xp_level_wizard_31.save()
    xp_level_wizard_32 = XPLevel()
    xp_level_wizard_32.xp_level_factory(wizard, 32, 1316000, 580)
    xp_level_wizard_32.save()
    xp_level_wizard_33 = XPLevel()
    xp_level_wizard_33.xp_level_factory(wizard, 33, 1389000, 617)
    xp_level_wizard_33.save()
    xp_level_wizard_34 = XPLevel()
    xp_level_wizard_34.xp_level_factory(wizard, 34, 1463000, 655)
    xp_level_wizard_34.save()
    xp_level_wizard_35 = XPLevel()
    xp_level_wizard_35.xp_level_factory(wizard, 35, 1538000, 694)
    xp_level_wizard_35.save()
    xp_level_wizard_36 = XPLevel()
    xp_level_wizard_36.xp_level_factory(wizard, 36, 1614000, 734)
    xp_level_wizard_36.save()

    xp_level_thief_2 = XPLevel()
    xp_level_thief_2.xp_level_factory(thief, 2, 325, 2)
    xp_level_thief_2.save()
    xp_level_thief_3 = XPLevel()
    xp_level_thief_3.xp_level_factory(thief, 3, 730, 4)
    xp_level_thief_3.save()
    xp_level_thief_4 = XPLevel()
    xp_level_thief_4.xp_level_factory(thief, 4, 1575, 8)
    xp_level_thief_4.save()
    xp_level_thief_5 = XPLevel()
    xp_level_thief_5.xp_level_factory(thief, 5, 3450, 12)
    xp_level_thief_5.save()
    xp_level_thief_6 = XPLevel()
    xp_level_thief_6.xp_level_factory(thief, 6, 7450, 18)
    xp_level_thief_6.save()
    xp_level_thief_7 = XPLevel()
    xp_level_thief_7.xp_level_factory(thief, 7, 16150, 25)
    xp_level_thief_7.save()
    xp_level_thief_8 = XPLevel()
    xp_level_thief_8.xp_level_factory(thief, 8, 35000, 32)
    xp_level_thief_8.save()
    xp_level_thief_9 = XPLevel()
    xp_level_thief_9.xp_level_factory(thief, 9, 60000, 41)
    xp_level_thief_9.save()
    xp_level_thief_10 = XPLevel()
    xp_level_thief_10.xp_level_factory(thief, 10, 88000, 51)
    xp_level_thief_10.save()
    xp_level_thief_11 = XPLevel()
    xp_level_thief_11.xp_level_factory(thief, 11, 119000, 61)
    xp_level_thief_11.save()
    xp_level_thief_12 = XPLevel()
    xp_level_thief_12.xp_level_factory(thief, 12, 153000, 73)
    xp_level_thief_12.save()
    xp_level_thief_13 = XPLevel()
    xp_level_thief_13.xp_level_factory(thief, 13, 190000, 86)
    xp_level_thief_13.save()
    xp_level_thief_14 = XPLevel()
    xp_level_thief_14.xp_level_factory(thief, 14, 230000, 99)
    xp_level_thief_14.save()
    xp_level_thief_15 = XPLevel()
    xp_level_thief_15.xp_level_factory(thief, 15, 278000, 114)
    xp_level_thief_15.save()
    xp_level_thief_16 = XPLevel()
    xp_level_thief_16.xp_level_factory(thief, 16, 329000, 130)
    xp_level_thief_16.save()
    xp_level_thief_17 = XPLevel()
    xp_level_thief_17.xp_level_factory(thief, 17, 367000, 147)
    xp_level_thief_17.save()
    xp_level_thief_18 = XPLevel()
    xp_level_thief_18.xp_level_factory(thief, 18, 417000, 164)
    xp_level_thief_18.save()
    xp_level_thief_19 = XPLevel()
    xp_level_thief_19.xp_level_factory(thief, 19, 469000, 183)
    xp_level_thief_19.save()
    xp_level_thief_20 = XPLevel()
    xp_level_thief_20.xp_level_factory(thief, 20, 523000, 203)
    xp_level_thief_20.save()
    xp_level_thief_21 = XPLevel()
    xp_level_thief_21.xp_level_factory(thief, 21, 579000, 224)
    xp_level_thief_21.save()
    xp_level_thief_22 = XPLevel()
    xp_level_thief_22.xp_level_factory(thief, 22, 637000, 245)
    xp_level_thief_22.save()
    xp_level_thief_23 = XPLevel()
    xp_level_thief_23.xp_level_factory(thief, 23, 697000, 268)
    xp_level_thief_23.save()
    xp_level_thief_24 = XPLevel()
    xp_level_thief_24.xp_level_factory(thief, 24, 759000, 292)
    xp_level_thief_24.save()
    xp_level_thief_25 = XPLevel()
    xp_level_thief_25.xp_level_factory(thief, 25, 833000, 317)
    xp_level_thief_25.save()
    xp_level_thief_26 = XPLevel()
    xp_level_thief_26.xp_level_factory(thief, 26, 889000, 343)
    xp_level_thief_26.save()
    xp_level_thief_27 = XPLevel()
    xp_level_thief_27.xp_level_factory(thief, 27, 956000, 369)
    xp_level_thief_27.save()
    xp_level_thief_28 = XPLevel()
    xp_level_thief_28.xp_level_factory(thief, 28, 1024000, 397)
    xp_level_thief_28.save()
    xp_level_thief_29 = XPLevel()
    xp_level_thief_29.xp_level_factory(thief, 29, 1093000, 426)
    xp_level_thief_29.save()
    xp_level_thief_30 = XPLevel()
    xp_level_thief_30.xp_level_factory(thief, 30, 1163000, 456)
    xp_level_thief_30.save()
    xp_level_thief_31 = XPLevel()
    xp_level_thief_31.xp_level_factory(thief, 31, 1234000, 487)
    xp_level_thief_31.save()
    xp_level_thief_32 = XPLevel()
    xp_level_thief_32.xp_level_factory(thief, 32, 1306000, 519)
    xp_level_thief_32.save()
    xp_level_thief_33 = XPLevel()
    xp_level_thief_33.xp_level_factory(thief, 33, 1379000, 552)
    xp_level_thief_33.save()
    xp_level_thief_34 = XPLevel()
    xp_level_thief_34.xp_level_factory(thief, 34, 1453000, 585)
    xp_level_thief_34.save()
    xp_level_thief_35 = XPLevel()
    xp_level_thief_35.xp_level_factory(thief, 35, 1528000, 620)
    xp_level_thief_35.save()
    xp_level_thief_36 = XPLevel()
    xp_level_thief_36.xp_level_factory(thief, 36, 1604000, 656)
    xp_level_thief_36.save()

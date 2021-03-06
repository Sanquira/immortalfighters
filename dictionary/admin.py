"""Admin module for dictionary."""
from django.conf import settings
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from markdownx.admin import MarkdownxModelAdmin

from dictionary.models.beast import BeastWeakness, BeastCategory, Beast, BeastAttack, BeastMobility
from dictionary.models.items import Item, Artefact
from dictionary.models.skill import Skill, SkillPoints
from dictionary.models.spell import Spell, SpellDiscipline, SpellDirection, ProfessionLimitation


# pylint: disable=all

#######################################
# Resources

class MobilityResource(resources.ModelResource):
    class Meta:
        model = BeastMobility


class AttackResource(resources.ModelResource):
    class Meta:
        model = BeastAttack


class BeastResource(resources.ModelResource):
    class Meta:
        model = Beast


class CategoryResource(resources.ModelResource):
    class Meta:
        model = BeastCategory


class WeaknessResource(resources.ModelResource):
    class Meta:
        model = BeastWeakness


class SpellResource(resources.ModelResource):
    class Meta:
        model = Spell


class SpellDisciplineResource(resources.ModelResource):
    class Meta:
        model = SpellDiscipline


class SpellDirectionResource(resources.ModelResource):
    class Meta:
        model = SpellDirection


class ProfessionLimitationResource(resources.ModelResource):
    class Meta:
        model = ProfessionLimitation


class ItemResources(resources.ModelResource):
    class Meta:
        model = Item


class ArtefactResources(resources.ModelResource):
    class Meta:
        model = Artefact


class SkillPointsResources(resources.ModelResource):
    class Meta:
        model = SkillPoints


class SkillResources(resources.ModelResource):
    class Meta:
        model = Skill


#######################################
# Inlines

class ProfessionLimitationInline(admin.TabularInline):
    model = ProfessionLimitation
    extra = 0


class AttackInline(admin.TabularInline):
    model = BeastAttack
    extra = 0


class MobilityInline(admin.TabularInline):
    model = BeastMobility
    extra = 0


#######################################
# Admins


class MobilityAdmin(ImportExportModelAdmin):
    resource_class = MobilityResource


class AttackAdmin(ImportExportModelAdmin):
    resource_class = AttackResource


class BeastAdmin(ImportExportModelAdmin, MarkdownxModelAdmin):
    resource_class = BeastResource
    filter_horizontal = ('weakness',)
    inlines = (AttackInline, MobilityInline)


class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource
    ordering = ('name',)


class WeaknessAdmin(ImportExportModelAdmin):
    resource_class = WeaknessResource
    ordering = ('group',)


class SpellAdmin(ImportExportModelAdmin, MarkdownxModelAdmin):
    resource_class = SpellResource
    inlines = (ProfessionLimitationInline,)
    filter_horizontal = ('directions',)


class SpellDisciplineAdmin(ImportExportModelAdmin):
    resource_class = SpellDisciplineResource


class SpellDirectionAdmin(ImportExportModelAdmin):
    resource_class = SpellDirectionResource


class ProfessionLimitationAdmin(ImportExportModelAdmin):
    resource_class = ProfessionLimitationResource


class ItemAdmin(ImportExportModelAdmin):
    resource_class = ItemResources
    ordering = ('name',)


class ArtefactAdmin(ImportExportModelAdmin):
    resource_class = ArtefactResources
    filter_horizontal = ('spells',)


class SkillPointsAdmin(ImportExportModelAdmin):
    resource_class = SkillPointsResources


class SkillAdmin(ImportExportModelAdmin):
    resource_class = SkillResources
    ordering = ('name', 'stat',)


if settings.DEBUG:
    admin.site.register(BeastMobility, MobilityAdmin)
    admin.site.register(BeastAttack, AttackAdmin)
    admin.site.register(BeastCategory, CategoryAdmin)
    admin.site.register(BeastWeakness, WeaknessAdmin)
    admin.site.register(SpellDiscipline, SpellDisciplineAdmin)
    admin.site.register(SpellDirection, SpellDirectionAdmin)
    admin.site.register(ProfessionLimitation, ProfessionLimitationAdmin)
    admin.site.register(SkillPoints, SkillPointsAdmin)
admin.site.register(Beast, BeastAdmin)
admin.site.register(Spell, SpellAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Artefact, ArtefactAdmin)
admin.site.register(Skill, SkillAdmin)

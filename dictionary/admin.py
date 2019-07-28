from django.contrib import admin
# Register your models here.
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from markdownx.admin import MarkdownxModelAdmin

from dictionary.models.category import Category
from dictionary.models.items import Item, Artefact
from dictionary.models.profession import BaseProfession, XPLevel
from dictionary.models.profession_limitation import ProfessionLimitation
from dictionary.models.race import Race
from dictionary.models.skill import Skill
from dictionary.models.spell import Spell, SpellDiscipline, SpellDirection


#######################################
# Resources

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


class RaceResource(resources.ModelResource):
    class Meta:
        model = Race


class BaseProfessionResource(resources.ModelResource):
    class Meta:
        model = BaseProfession


class XPLevelResource(resources.ModelResource):
    class Meta:
        model = XPLevel


class ItemResources(resources.ModelResource):
    class Meta:
        model = Item


class ArtefactResources(resources.ModelResource):
    class Meta:
        model = Artefact


class CategoryResources(resources.ModelResource):
    class Meta:
        model = Category


class SkillResources(resources.ModelResource):
    class Meta:
        model = Skill


#######################################
# Inlines
# class SpellDisciplineLimitationInline(admin.TabularInline):
#     model = SpellDisciplineLimitation
#     extra = 0
#     filter_horizontal = ('directions',)


class ProfessionLimitationInline(admin.TabularInline):
    model = ProfessionLimitation
    extra = 0


#######################################
# Admins
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


class RaceAdmin(ImportExportModelAdmin):
    resource_class = RaceResource
    ordering = ('name',)


class BaseProfessionAdmin(ImportExportModelAdmin):
    resource_class = BaseProfessionResource
    ordering = ('parentProf', 'name',)


class XPLevelAdmin(ImportExportModelAdmin):
    resource_class = XPLevelResource


class ItemAdmin(ImportExportModelAdmin):
    resource_class = ItemResources
    ordering = ('name',)


class ArtefactAdmin(ImportExportModelAdmin):
    resource_class = ArtefactResources
    filter_horizontal = ('spells',)


class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResources


class SkillAdmin(ImportExportModelAdmin):
    resource_class = SkillResources
    ordering = ('name', 'stat',)


admin.site.register(Spell, SpellAdmin)
admin.site.register(SpellDiscipline, SpellDisciplineAdmin)
admin.site.register(SpellDirection, SpellDirectionAdmin)
# admin.site.register(SpellDisciplineLimitation, SpellDisciplineLimitationAdmin)
admin.site.register(ProfessionLimitation, ProfessionLimitationAdmin)
admin.site.register(Race, RaceAdmin)
admin.site.register(BaseProfession, BaseProfessionAdmin)
admin.site.register(XPLevel, XPLevelAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Artefact, ArtefactAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Skill, SkillAdmin)

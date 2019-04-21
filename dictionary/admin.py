from django.contrib import admin
# Register your models here.
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from dictionary.models import *


class SpellResource(resources.ModelResource):
    class Meta:
        model = Spell


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


class SpellAdmin(ImportExportModelAdmin):
    resource_class = SpellResource


class ProfessionLimitationAdmin(ImportExportModelAdmin):
    resource_class = ProfessionLimitationResource


class RaceAdmin(ImportExportModelAdmin):
    resource_class = RaceResource


class BaseProfessionAdmin(ImportExportModelAdmin):
    resource_class = BaseProfessionResource


class XPLevelAdmin(ImportExportModelAdmin):
    resource_class = XPLevelResource


admin.site.register(Spell, SpellAdmin)
admin.site.register(ProfessionLimitation, ProfessionLimitationAdmin)
admin.site.register(Race, RaceAdmin)
admin.site.register(BaseProfession, BaseProfessionAdmin)
admin.site.register(XPLevel, XPLevelAdmin)

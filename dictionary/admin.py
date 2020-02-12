"""Admin module for dictionary."""
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from markdownx.admin import MarkdownxModelAdmin

from dictionary.models.beast import Beast, BeastAttack, BeastMobility
from dictionary.models.items import Artefact
from dictionary.models.spell import Spell, ProfessionLimitation


#######################################
# Inlines

class ProfessionLimitationInline(admin.TabularInline):
    """Inline Admin view for ProfessionLimitation"""
    model = ProfessionLimitation
    extra = 0


class AttackInline(admin.TabularInline):
    """Inline Admin view for BeastAttack"""
    model = BeastAttack
    extra = 0


class MobilityInline(admin.TabularInline):
    """Inline Admin view for BeastMobility"""
    model = BeastMobility
    extra = 0


#######################################
# Admins

@admin.register(Beast)
class BeastAdmin(ImportExportModelAdmin, MarkdownxModelAdmin):
    """Model admin for Beast"""
    filter_horizontal = ('weakness',)
    inlines = (AttackInline, MobilityInline)


@admin.register(Spell)
class SpellAdmin(ImportExportModelAdmin, MarkdownxModelAdmin):
    """Model admin for Spell"""
    inlines = (ProfessionLimitationInline,)
    filter_horizontal = ('directions',)


@admin.register(Artefact)
class ArtefactAdmin(ImportExportModelAdmin):
    """Model admin for Artefact"""
    filter_horizontal = ('spells',)

"""Admin module for base."""
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from base.forms.auth_form import IFUserCreationForm, IFUserChangeForm
from base.models.character import Character
from base.models.ifuser import IFUser
from base.models.profession import BaseProfession, XPLevel
from base.models.race import Race
from base.models.sizes import CreatureSize
from django.utils.translation import gettext, gettext_lazy as _


# pylint: disable=all

#######################################
# Resources

class CreatureSizeResource(resources.ModelResource):
    class Meta:
        model = CreatureSize


class RaceResource(resources.ModelResource):
    class Meta:
        model = Race


class BaseProfessionResource(resources.ModelResource):
    class Meta:
        model = BaseProfession


class XPLevelResource(resources.ModelResource):
    class Meta:
        model = XPLevel


#######################################
# Admins


class CreatureSizeAdmin(ImportExportModelAdmin):
    resource_class = CreatureSizeResource
    ordering = ('name',)


class RaceAdmin(ImportExportModelAdmin):
    resource_class = RaceResource
    ordering = ('name',)


class BaseProfessionAdmin(ImportExportModelAdmin):
    resource_class = BaseProfessionResource
    ordering = ('parent_prof', 'name',)


class XPLevelAdmin(ImportExportModelAdmin):
    resource_class = XPLevelResource
    ordering = ('profession', 'level')


class IFUserAdmin(ImportExportModelAdmin, UserAdmin):
    model = IFUser
    list_display = ['username', 'last_login', 'active_char', 'email']
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        ('Postava', {'fields': ('active_char',)}),
        ('Další', {'fields': ('chat_color',)}),
    )


if settings.DEBUG:
    admin.site.register(CreatureSize, CreatureSizeAdmin)
    admin.site.register(Race, RaceAdmin)
    admin.site.register(BaseProfession, BaseProfessionAdmin)
    admin.site.register(XPLevel, XPLevelAdmin)
admin.site.register(Character)
admin.site.register(IFUser, IFUserAdmin)

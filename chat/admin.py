"""
Resources for Django administration
"""
# pylint: disable=all

from django.contrib import admin
#######################################
# Resources
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from markdownx.admin import MarkdownxModelAdmin

from chat.models import Room


class RoomResource(resources.ModelResource):
    class Meta:
        model = Room


#######################################
# Admins

class RoomAdmin(ImportExportModelAdmin, MarkdownxModelAdmin):
    resource_class = RoomResource


admin.site.register(Room, RoomAdmin)

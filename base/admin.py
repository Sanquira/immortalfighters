"""Admin module for base."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin

from base.models.ifuser import IFUser


@admin.register(IFUser)
class IFUserAdmin(ImportExportModelAdmin, UserAdmin):
    """Admin model for IFUser"""
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

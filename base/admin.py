from django.contrib import admin

# Register your models here.
from base.models import IFUser
from base.models.character import Character

admin.site.register(Character)
admin.site.register(IFUser)

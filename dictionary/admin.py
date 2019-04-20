from django.contrib import admin

# Register your models here.
from dictionary.models import *

admin.site.register(Spell)
admin.site.register(ProfessionLimitation)
admin.site.register(Race)
admin.site.register(BaseProfession)
admin.site.register(XPLevel)

from django.contrib import admin

# Register your models here.
from guilds.models import *

admin.site.register(Content)
admin.site.register(Guild)
admin.site.register(Rank)
admin.site.register(Thread)
admin.site.register(Transaction)
admin.site.register(CharacterInGuildWithRank)
admin.site.register(RankGuildPermission)
admin.site.register(RankThreadPermission)



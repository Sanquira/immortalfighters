from django.db import models
from base.models import Character
from guilds.models import Guild,Rank


class CharacterInGuildWithRank(models.Model):
    character = models.ForeignKey(Character,on_delete=models.CASCADE,related_name='+')
    guild = models.ForeignKey(Guild,on_delete=models.CASCADE)
    rank = models.ForeignKey(Rank,on_delete=models.CASCADE)
from django.db import models
from guilds.models import Guild


class Thread(models.Model):
    guild = models.ForeignKey(Guild,on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
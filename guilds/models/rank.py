from django.db import models
from guilds.models import Guild
from enum import Enum


class PermissionType(Enum):
    NONE = 'None'
    READ = 'Read'
    WRITE= 'Write'
    ADMIN= 'Admin'


class Rank(models.Model):
    guild = models.ForeignKey(Guild,on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
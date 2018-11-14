from django.db import models
from base.models import Character
from guilds.models import Guild,Thread


class Content(models.Model):
    author = models.ForeignKey(Character,on_delete=models.CASCADE,related_name='+')
    guild = models.ForeignKey(Guild,on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    content = models.TextField()
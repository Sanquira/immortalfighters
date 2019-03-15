from django.db import models

from base.models import IFUser


class Character(models.Model):
    owner = models.ForeignKey(IFUser, on_delete=models.CASCADE)
    characterName = models.CharField(max_length=30)

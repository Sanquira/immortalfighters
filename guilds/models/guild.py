from django.db import models


class Guild(models.Model):
    name = models.CharField(max_length=45)
    icon = models.ImageField()

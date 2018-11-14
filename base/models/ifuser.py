from django.db import models


class IFUser(models.Model):
    username = models.CharField(max_length=30)

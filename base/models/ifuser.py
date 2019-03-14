from django.db import models
from django.contrib.auth.models import AbstractUser


class IFUser(AbstractUser, models.Model):
    username = models.CharField(max_length=30, unique=True)
    pass

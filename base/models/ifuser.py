from django.contrib.auth.models import AbstractUser
from django.db import models


class IFUser(AbstractUser, models.Model):
    pass

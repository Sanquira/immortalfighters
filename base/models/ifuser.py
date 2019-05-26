from django.contrib.auth.models import AbstractUser
from django.db import models


class IFUser(AbstractUser, models.Model):
    active_char = models.ForeignKey("Character", on_delete=models.CASCADE, null=True, blank=True,
                                    verbose_name="Aktivní postava")

    class Meta:
        verbose_name = "Uživatel"
        verbose_name_plural = "Uživatelé"

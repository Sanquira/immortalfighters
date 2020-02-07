"""Module for IFUser entity."""
from django.contrib.auth.models import AbstractUser
from django.db import models

from utils.models.color_field import ColorField


class IFUser(AbstractUser, models.Model):
    """
    Use model for IF. It replaces default django User model.
    """
    active_char = models.ForeignKey("Character", on_delete=models.CASCADE, null=True, blank=True,
                                    verbose_name="Aktivní postava")
    chat_color = ColorField(default='#ffffff', null=False, blank=False, verbose_name="Barva chatu")

    class Meta:
        verbose_name = "Uživatel"
        verbose_name_plural = "Uživatelé"

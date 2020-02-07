"""
Models required for the chat application
"""
from django.db import models


class LowerCaseCharField(models.CharField):
    """CharField that contains only lowercase symbols"""

    def get_prep_value(self, value):
        return str(value).lower()


class Room(models.Model):
    """Chat single_room"""
    name = LowerCaseCharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Místnost"
        verbose_name_plural = "Místnosti"

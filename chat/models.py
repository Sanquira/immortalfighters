"""
Models required for the chat application
"""
from django.contrib import admin
from django.contrib.postgres.fields import JSONField
from django.core.serializers.json import DjangoJSONEncoder
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


class HistoryRecord(models.Model):
    """History record for chat messages"""
    room = models.ForeignKey(Room, on_delete=models.CASCADE, db_index=True)
    time = models.DateTimeField(db_index=True)
    message = JSONField(encoder=DjangoJSONEncoder)

    class Meta:
        ordering = ['-time']


admin.site.register(HistoryRecord)

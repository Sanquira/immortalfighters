from django.db import models


# Create your models here.
from markdownx.models import MarkdownxField

from dungeon.fields import LuaField, StringIdentifier


class Event(models.Model):
    dungeon = models.ForeignKey("Dungeon", on_delete=models.CASCADE)
    name = StringIdentifier(max_length=30)
    description = MarkdownxField(null=True, blank=True)
    on_enter = LuaField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['dungeon', 'name'], name='unique-dungeon-name'),
        ]


class Option(models.Model):
    class Type(models.IntegerChoices):
        CLICK = 0
        TEXT_INPUT = 1

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = StringIdentifier(max_length=30)
    description = MarkdownxField(null=True, blank=True)
    on_click = LuaField(null=True, blank=True)
    type = models.IntegerField(choices=Type.choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['event', 'name'], name='unique-option-name'),
        ]


class Dungeon(models.Model):
    first_event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, db_index=False, related_name='+')
    name = models.CharField(max_length=30)
    description = MarkdownxField(null=True, blank=True)

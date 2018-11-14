from enum import Enum
from django.db import models
from base.models import Character
from guilds.models import Guild


class TransactionType(Enum):
    money = 'Money transaction'
    rep = 'Reputation transaction'


class Transaction(models.Model):
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE)
    sender = models.ForeignKey(Character, on_delete=models.CASCADE,related_name='+')
    receiver = models.ForeignKey(Character, on_delete=models.CASCADE,related_name='+')
    type = models.CharField(max_length=10, choices=[(tag, tag.value) for tag in TransactionType],
                            default=TransactionType.money)
    message = models.TextField()
    amount = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)
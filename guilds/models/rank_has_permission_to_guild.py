from django.db import models
from guilds.models import Rank,PermissionType


class RankGuildPermission(models.Model):
    rank = models.OneToOneField(Rank, on_delete=models.CASCADE)
    guildPerm = models.CharField(max_length=10, choices=[(tag, tag.value) for tag in PermissionType],
                                 default=PermissionType.READ)
    # TransactionType
    bankPerm = models.CharField(max_length=10, choices=[(tag, tag.value) for tag in PermissionType],
                                     default=PermissionType.READ)

    boardPerm = models.CharField(max_length=10, choices=[(tag, tag.value) for tag in PermissionType],
                                 default=PermissionType.READ)

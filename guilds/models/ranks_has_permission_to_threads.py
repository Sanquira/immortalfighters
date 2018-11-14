from django.db import models
from guilds.models import PermissionType,Rank,Thread


class RankThreadPermission(models.Model):
    rank = models.ForeignKey(Rank,on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread,on_delete=models.CASCADE)
    threadPerm = models.CharField(max_length=10, choices=[(tag, tag.value) for tag in PermissionType],
                                 default=PermissionType.READ)
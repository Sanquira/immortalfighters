from django.db import models


class LowerCaseCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(LowerCaseCharField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()


# Create your models here.
class Room(models.Model):
    name = LowerCaseCharField(max_length=30, unique=True)
    permission_needed = models.CharField(max_length=50, null=True)

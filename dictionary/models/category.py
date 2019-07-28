from enum import Enum

from django.db import models


class CategoryType(Enum):
    ITEM = "Předmět"
    BEAST = "Nestvůra"


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Kategorie")
    parent = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Nadkategorie")

    def get_all_children(self, include_self=True):
        r = []
        if include_self:
            r.append(self)
        for c in Category.objects.filter(parent=self):
            _r = c.get_all_children(include_self=True)
            if len(_r) > 0:
                r.extend(_r)
        return r

    def __str__(self):
        if self.parent is None:
            return self.name
        return self.parent.__str__() + " -> " + self.name

    class Meta:
        verbose_name = "Kategorie"
        verbose_name_plural = verbose_name

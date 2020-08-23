"""Module for Color field."""
from django.db import models

from utils.widgets import ColorWidget


class ColorField(models.CharField):
    """
    ColorField extended CharField for saving color in db.
    Specifies custom color widget.
    """

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = ColorWidget
        return super().formfield(**kwargs)

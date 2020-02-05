"""Module for widgets."""
from django.forms.widgets import Input


class ColorWidget(Input):
    """
    Widget for ColorField.
    """
    input_type = 'color'
    template_name = 'color.html'

"""Module for boolean type check filter in templates."""
from django import template

register = template.Library()


@register.filter
def is_boolean(value):
    """
    Filter checking if value variable is bool type.
    Used for template->JS type conversion.
    :param value:
    :return:
    """
    return isinstance(value, bool)

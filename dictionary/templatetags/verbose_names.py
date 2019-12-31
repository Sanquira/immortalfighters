"""Module for get_verbose_field_name."""
from django import template
from django.core.exceptions import FieldDoesNotExist
from django.db import models

register = template.Library()


@register.simple_tag
def get_verbose_field_name(instance, field_name):
    """
    Returns verbose_name for a field.
    """
    try:
        if isinstance(instance._meta.get_field(field_name), models.ManyToOneRel):
            return instance._meta.get_field(field_name).related_model._meta.verbose_name
        return instance._meta.get_field(field_name).verbose_name
    except FieldDoesNotExist:
        return field_name

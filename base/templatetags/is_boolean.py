from django import template

register = template.Library()


@register.filter
def is_boolean(value):
    return isinstance(value, bool)

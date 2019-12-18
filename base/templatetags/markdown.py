from django import template
from django.template.defaultfilters import stringfilter
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

register = template.Library()


@register.filter
@stringfilter
def show_markdown(text):
    return markdownify(text)


@register.simple_tag
def is_markdown(instance, field_name):
    return isinstance(instance._meta.get_field(field_name), MarkdownxField)

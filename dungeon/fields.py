from django.db.models import TextField

from chat.models import LowerCaseCharField


class LuaField(TextField):
    """Field for storing lua code, to be finished"""


class StringIdentifier(LowerCaseCharField):
    """String identifier for specific entity, must be uniquely serializable to url path"""

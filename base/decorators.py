"""Module for decorators."""
from functools import wraps

from django.core.exceptions import PermissionDenied


def character_required(func):
    """
    Decorator which test if user has active character.
    Raise PermissionDenied if there is no active character, call decorated function otherwise.
    """

    @wraps(func)
    def _test_character(request, *args, **kwargs):
        if request.character is not None:
            return func(request, *args, **kwargs)

        raise PermissionDenied("Stránka požaduje mít aktivní charakter")

    return _test_character

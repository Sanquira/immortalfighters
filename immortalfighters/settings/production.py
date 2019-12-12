"""
Production deployment settings
python manage.py migrate --settings=immortalfighters.settings.production
"""
# pylint: disable=wildcard-import,unused-wildcard-import
from .base import *

DEBUG = False

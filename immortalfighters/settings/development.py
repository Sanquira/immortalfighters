"""
Development settings
Don't require specific configuration, are set as default ones
"""
# pylint: disable=wildcard-import,unused-wildcard-import
from .base import *

DEBUG = True

ALLOWED_HOSTS = ["0.0.0.0", "localhost", "127.0.0.1"]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

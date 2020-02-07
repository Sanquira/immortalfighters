"""
Settings used for tests
"""
# pylint: disable=wildcard-import,unused-wildcard-import
from .development import *
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5433',
        'CONN_MAX_AGE': 0
    }
}

CHAT_HISTORY_MESSAGES = 3

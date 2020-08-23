"""
Settings used for tests
"""
# pylint: disable=wildcard-import,unused-wildcard-import
from immortalfighters.settings.base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
    }
}

USE_TZ = False

CHAT_HISTORY_MESSAGES = 3

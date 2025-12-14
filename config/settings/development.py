"""
Development settings
"""

from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Development-specific settings
INSTALLED_APPS += [
    'django_extensions',  # Optional: adds shell_plus and other useful commands
]

# Database for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

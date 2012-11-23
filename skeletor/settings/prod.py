from .base import *

DEBUG = TEMPLATE_DEBUG = False

# Try to use DATABASE_URL environment variable if possible, otherwise fall back
# to hardcoded values
try:
    import dj_database_url
    DATABASES = {'default': dj_database_url.config()}
except ImportError:
    DATABASES = {}

if not DATABASES or not DATABASES.get('default'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': '',                      # Or path to database file if using sqlite3.
            'USER': '',                      # Not used with sqlite3.
            'PASSWORD': '',                  # Not used with sqlite3.
            'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }
    }

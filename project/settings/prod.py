from .base import *

DEBUG = TEMPLATE_DEBUG = False
COMPRESS_ENABLED = True

# Uncomment to precompress files during deployment (also update Makefile)
# COMPRESS_OFFLINE = True

# Try to use DATABASE_URL environment variable if possible, otherwise fall back
# to hardcoded values
try:
    import dj_database_url
    DATABASES = {'default': dj_database_url.config()}
except ImportError:
    DATABASES = {}

if not DATABASES or 'default' not in DATABASES:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.',
            'NAME': '',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    }

# Memcached is better choice, if you can set it up; if not, this is a good
# alternative.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Enable Raven if it's installed
try:
    import raven.contrib.django.raven_compat  # noqa
    INSTALLED_APPS += ('raven.contrib.django.raven_compat',)

    # Raven will try to use SENTRY_DSN from environment if possible (eg. on
    # Heroku). If you need to set it manually, uncomment and set SENTRY_DSN
    # setting here.
    # SENTRY_DSN = ''
except ImportError:
    pass

# Enable gunicorn if it's installed
try:
    import gunicorn  # noqa
    INSTALLED_APPS += (
        'gunicorn',
    )
except ImportError:
    pass

# Enable django-compressor if it's installed
try:
    import compressor  # noqa
    INSTALLED_APPS += ('compressor',)
except ImportError:
    pass

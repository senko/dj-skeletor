# Settings file optimized for test running. Sets up in-memory database
# and disables South and Sentry for the tests

from .base import *

# Use in-memory SQLIte3 database for faster tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# No need to use South in testing
SOUTH_TESTS_MIGRATE = False
SKIP_SOUTH_TESTS = True

# Disable Sentry if it was installed
INSTALLED_APPS = [app for app in INSTALLED_APPS
    if not app.startswith('raven.')]
MIDDLEWARE_CLASSES = [cls for cls in MIDDLEWARE_CLASSES
    if not cls.startswith('raven.')]
LOGGING = BASE_LOGGING

# Disable cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

try:
    import django_nose
    INSTALLED_APPS += (
        'django_nose',
    )
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
except ImportError:
    pass

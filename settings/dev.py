from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db',
    }
}

# Django Debug Toolbar

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
INSTALLED_APPS += (
    'debug_toolbar',
)
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': lambda *args, **kwargs: True
}

# Sentry - use even in debug mode

SENTRY_TESTING = True

# make Sentry sensitive to DEBUG output
for app, cfg in LOGGING['loggers'].items():
    if 'sentry' in cfg['handlers']:
        cfg['level'] = 'DEBUG'

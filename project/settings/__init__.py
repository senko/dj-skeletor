# Try to activate local settings. If it fails, assume we're on production and
# activate production settings. Note that local.py shouldn't be tracked in the
# repository.

try:
    from .local import *
except ImportError:
    from .prod import *

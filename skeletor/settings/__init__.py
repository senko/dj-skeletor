# Create a separate local config for each of the environments the app will
# run in. Store all the configs in git. To activate a particular configuration,
# symlink settings/local.py to it. Do not store the symlink in the git repo.
from .local import *

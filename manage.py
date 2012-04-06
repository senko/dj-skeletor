#!/usr/bin/env python
from os import environ, listdir
from os.path import join, dirname, abspath, exists
import sys

if __name__ == "__main__":

    # Try to discover project name and set the default settings module
    # based on it. If discovery fails, DJANGO_SETTINGS_MODULE environment
    # variable must be set.

    root = dirname(abspath(__file__))
    sys.path.append(root)
    settings_module = None
    for name in listdir(root):
        full_name = join(root, name)
        if (exists(join(full_name, 'settings.py')) or
            exists(join(full_name, 'settings.pyc')) or
            exists(join(full_name, 'settings', '__init__.py')) or
            exists(join(full_name, 'settings', '__init__.pyc'))):
                settings_module = name + '.settings'
                break

    if settings_module is not None:
        environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

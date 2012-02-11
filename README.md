## DJ Skeletor

DJ Skeletor is a skeleton Django project handy for bootstrapping new
empty projects.

The repository contains an empty, relocatable Django project with South,
Django Debug Toolbar and Sentry apps set, and with provisions for test and
production settings.


### Quick setup

    # prepare the virtual environment
    virtualenv --no-site-packages myenv
    cd myenv
    source bin/activate

    # get the skeleton project
    git clone https://github.com/senko/dj-skeletor.git myproject
    cd myproject

    # install requirements
    pip install -r requirements.txt

    # activate dev environment
    cd settings
    ln -s dev.py local.py
    cd ..
    python manage.py syncdb
    python manage.py migrate sentry

    # run it!
    python manage.py runserver


### Settings

Settings are handled in the *settings* module:

  * settings.base - base/invariant project settings
  * settings.dev - development/test environment
  * settings.prod - production environment
  * settings.local - a symlink to current environment settings

To activate the specific environment, symlink settings/local.py (not
in the repository for obvious reasons) to either prod or dev (or some
other, if you need more different enviroments) settings module.

### Django Debug Toolbar

Django Debug Toolbar is set up so it's always visible in the dev
environment, no matter what the client IP is, and always hidden in
the production environment.

### Database

A simple sqlite3 database is configured in the settings, so no additional
configuration is needed to start hacking right away. South is used for
schema migrations.

### Sentry

Sentry is used in the integrated setup, ie. as an app inside the Django
project. This makes things simpler when starting. When the project grows,
or if you have several apps you need to monitor, consider switching to
running Sentry in Client/Server mode.

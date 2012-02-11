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

    # initialize the database
    python manage.py syncdb
    python manage.py migrate

    # run it!
    python manage.py runserver


### Settings

Settings are handled in the *settings* module:

  * settings.base - base/invariant project settings
  * settings.dev - development/test environment
  * settings.prod - production environment
  * settings.local - local environment

If you're storing your environment settings in the repository, the easiest
way to activate it on the server is to symlink settings/local.py to either
prod or dev settings module.

If you like to keep the local settings out of the git repository, use dev.py
or prod.py as a template and create your local.py as needed.

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
running Sentry in client/server mode.

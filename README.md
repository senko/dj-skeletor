## DJ Skeletor

DJ Skeletor is a skeleton Django project handy for bootstrapping new
empty projects.

The repository contains an empty, relocatable Django project with South,
Django Debug Toolbar and Raven apps set, and with provisions for development,
test and production settings.


### Features

Comes with:

  * South for database migrations
  * Django Debug Toolbar for displaying extra information about your view excution
  * Sentry client for logging exceptions (and custom logging)
  * Fabric for easy deployment to remote servers
  * Test-specific settings for running test with an in-memory SQLite database
  * SQLite database configured in the default development settings

DJ Skeletor requires Django 1.4 or later. All the other requirements are
optional and can be disabled.


### Quick setup

    # prepare the virtual environment
    mkvirtualenv --no-site-packages myenv

    # get the skeleton project
    git clone https://github.com/senko/dj-skeletor.git myproject
    cd myproject

    # install requirements
    pip install -r requirements.txt

    # rename the project directory to reflect your project name
    git mv skeletor myproject && git commit -m 'renamed project'

    # activate dev environment
    echo 'from .dev import *' > myproject/settings/local.py

    # initialize the database
    python manage.py syncdb
    python manage.py migrate

    # collect the static files needed by the apps
    python manage.py collectstatic --noinput

    # run it!
    python manage.py runserver


### Settings

Settings are handled in the *settings* module:

  * settings.base - base/invariant project settings
  * settings.dev - development environment
  * settings.prod - production environment
  * settings.test - test environment
  * settings.local - local environment

If you're storing your environment settings in the repository, the easiest
way to activate it on the server is to symlink settings/local.py to either
prod or dev settings module.

If you like to keep the local settings out of the git repository, use dev.py
or prod.py as a template and create your local.py as needed. The quick
setup procedure and fabric setup tasks create a simple local.py that just
imports everything from the development environment.

Test settings are separate to make it easier to customize settings for use
when running unit tests. The default test settings use in-memory SQLite
database and turn off South migrations and Sentry logging.

### Django Debug Toolbar

Django Debug Toolbar is set up so it's always visible in the dev
environment, no matter what the client IP is, and always hidden in
the production environment.

### Database

A simple sqlite3 database is configured in the development settings, so
no additional configuration is needed to start hacking right away. South
is used for schema migrations.

The database filename used is 'dev.db' in the project root directory. It is
explicitly ignored by git and fabric when rsyncing the local directory to server.


### Sentry / Raven

To use the Sentry client, you'll need a server to point it to. Installing
Sentry server is easy as:

    # mkvirtualenv --no-site-packages sentry-env
    # pip install sentry
    # sentry init
    # sentry start

You'll want to install Sentry into its own environment as it requires
Django 1.2 or 1.3 at the moment.

If you don't want to install Sentry yourself, you can use a hosted
version at http://getsentry.com/.

When you connect to your (or hosted) Sentry server and create a new project
there, you'll be given Sentry DSN which you need to put into settings/base.py
to activate Sentry logging.

### Fabric

A fabfile is provided with common tasks for rsyncing local directory to
the server for use while developing the project, and for deploying the
project using git clone/pull.

Useful commands:

  * server - host to connect to (same as -H, but accepts only one argument)
  * env - virtualenv name on the server, as used with virtualenvwrapper/workon
  * project_path - full path to the project directory on the server
  * rsync - use rsync to copy the local folder to the project directory on the server
  * setup - set up the project instance on the server (clones the origin
    repository, creates a virtual environment, initialises the database and
    runs the tests)
  * deploy - deploy a new version of project on the server using git pull
  * collecstatic, syncdb, migrate, runserver - run manage.py command
  * update - combines collecstatic, syncdb, migrate
  * test - run manage.py test with the test settings enabled

For all the commands, run <code>fab -l</code> or look at the source.

#### Examples:

Copy local directory to the server, update database and static files, and
run tests (only files changed from last copy are going to be copied):

    fab server:my.server.com env:myenv project_path:/path/to/project rsync update test

Deploy a new instance of a project on a server ('myenv' will be newly created,
code will be cloned into /path/to/project):

    fab server:my.server.com env:myenv project_path:/path/to/project \
        setup:origin=http://github.com/senko/dj-skeletor

Deploy a new version of the project on the server (a new git tag will be
created for each deployment, so it's easy to roll-back if needed):

    fab server:my.server.com env:myenv project_path:/path/to/project deploy

##### Customization

Everyone has a slightly different workflow, so you'll probably want to
customize the default fabric tasks or combine them. You can either customize
fabfile.py and commit the changes to your repository, or you can create
local_fabfile.py, which will be loaded if it exists. The latter can be useful
if you have per-team-member fabric customizations you don't want to commit
to the repository.

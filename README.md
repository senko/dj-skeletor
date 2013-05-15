# DJ Skeletor

DJ Skeletor is a skeleton Django project handy for quick bootstrapping of new
empty Django projects. It will help you get up and running with your project
in seconds.

The repository contains an empty, relocatable Django project with a selection
of useful Django application and setup for development, production and
(automated) test settings and environments.

### Quickstart

    # prepare the virtual environment
    mkvirtualenv --no-site-packages myenv

    # get the skeleton project
    git clone https://github.com/senko/dj-skeletor.git myproject
    cd myproject

    # set up the development environment
    make dev-setup

    # run your fully operational Django project
    python manage.py runserver_plus

### Batteries included

The development environment by default includes:

* [South](http://south.readthedocs.org/en/latest/about.html)
  for database migrations (both development and production use it)
* [Django Debug Toolbar](https://github.com/django-debug-toolbar/django-debug-toolbar)
  for displaying extra information about view execution
* SQLite database (`dev.db` in the project root directory)
* Integrated view debugger making it easy to debug crashes directly from the
  browser (Werkzeug and django-extension's
  [runserver_plus](http://pythonhosted.org/django-extensions/runserver_plus.html))
* Full SQL statement logging
* Beefed-up Django shell with model auto-loading and
  [IPython](http://ipython.org/) REPL
* [Flake8](https://pypi.python.org/pypi/flake8) source code checker
  (style, passive code analysis)
* Console E-mail backend set by default in dev for simple E-mail send testing
* Automated testing all set-up with
  [nose](https://nose.readthedocs.org/en/latest/), optionally creating test
  coverage reports, and using the in-memory SQLite database (and disabled
  South) to speed up test execution
* Disabled cache for easier debugging

The production environment by default includes:

* South for database migrations (both development and production use it)
* [Gunicorn](http://gunicorn.org/) integration
* [Django Compressor](http://django_compressor.readthedocs.org/en/master/)
  for CSS/JS asset minification and compilation
* Database auto-discovery via environment settings, compatible with Heroku
* [Sentry](http://sentry.readthedocs.org/en/latest/) client (raven\_compat)
  for exception logging (used only if `SENTRY_DSN` variable is set in
  settings or environment)
* Local-memory cache (although memcached is strongly recommended if available)

### The extended tour

After setting up your new Django project (see Quickstart above), try these:

    # make sure all tests pass (you'll need to write them first, though :)
    make test

    # get a test coverage report (outputs to stdout, saves HTML format in
    # cover/index.html and produces Cobertura report compatible with Jenkins)
    make coverage

    # clean up test artifacts, *.pyc files and cached compressed assets
    make clean

    # check if the code follows PEP8 and is free of obvious errors
    # this also includes cyclomatic complexity check and will complain if your
    # code is too complex (configurable by editing the Makefile)
    make lint

    # update the environment (eg. after pulling in new code)
    make dev-update

    # open up the new and improved Django shell
    python manage.py shell_plus

Yearn for more? Django-extension comes with tons of useful management commands,
run `python manage.py help` to get an overview.

### The production setup

The production environment can't be set up automatically (at it may require
setting up databaes details and other per-server settings manually), but there
are some helper Makefile tasks to speed it up.

To set up the production environment for a DJ Skeletor-powered project, loosely
follow this procedure:

    # prepare the virtual environment
    mkvirtualenv --no-site-packages myenv

    # get your project
    git clone <myproject-url>
    cd myproject

    # install the requirements
    make reqs/prod

    # create a project/settings/local.py settings file with per-server config
    vim project/settings/local.py

    # run automatic update (db sync/migrations, collectstatic)
    make prod-update

    # your production environment is now ready
    python manage.py run_gunicorn

Of course, your mileage may vary.

### The settings files

The settings files `base` (base settings used in all environments),
`prod` (production settings), `dev` (local development settings) and
`test` (settings used when running automated tests) should contain only the
settings used by all developers/servers.

Per-server (or per-developer) settings should go into `local` module
(ie. `project/settings/local.py`). The usual pattern for this module is to
first import everything from the settings variant that best matches your
environment (`prod` for servers, `dev` for local development), and then
override/add settings as needed.

Example production settings just specifying the production database:

    # file: project/settings/local.py
    from .prod import *

    DATABASES = {
        'default': { ... }
    }

You shouldn't need to add `local.py` to the repository (in fact, git is
already set up to ignore it). If some setting needs to be shared by everyone,
it should probably be added to `base`, `dev` or `prod`.

The local settings file isn't required. If it doesn't exist, the production
setup will be used by default. This is useful if you don't have per-server
settings or they're deployed via Unix environment (as they are on eg. Heroku
and similar cloud hosting providers).

### Heroku support

The production setup uses database autodiscovery so if you have a (promoted)
database in Heroku, it will automatically get picked up.

For Heroku, you'll probably want to add the `Procfile` file with contents
similar to this:

    web: python manage.py run_gunicorn --workers=4 --bind=0.0.0.0:$PORT

If your web app supports uploading of media (eg. images, videos or other
files) by users, you'll probably need the `django-storages` app to
automatically host them somewhere else (eg on Amazon S3). When
`django-storages` is set up, the collecstatic management command (run as
part of `make prod-update`) will copy the static assets to the specified
service as well.

After pushing the new code to Heroku for update, you should make sure to run
all the needed management commands to migrate the database, etc:

    heroku run make prod-update

### Django Debug Toolbar

Django Debug Toolbar is set up so it's always visible in the dev
environment, no matter what the client IP is, and always hidden in
the production environment.

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
there, you'll be given Sentry DSN which you need to put into production
settings to activate Sentry exception logging.

### Compressor

Django Compressor can minify and compile your CSS and JS assets. DJ Skeletor
comes with Compressor support, but to make use of it, you need to use
`{% compress %}` tags in your templates.

By default Compressor runs in online mode, and files are compressed
and cached (if needed) when the template that uses them is first served.
Optionally, it can also use offline mode (COMPRESSOR_OFFLINE) in which
the static files are pre-compressed in deployment phase. To activate this,
you'll need to activate the `COMPRESSOR_OFFLINE` setting (it's commented
out in `settings/prod.py` by default) and update `Makefile` to run the
compressor in the deployment phase.

Note that if you enable offline mode, you will need to run compress after
every template or static file change, so it's recommended to only use it
for deployed/production environments.

### Test code coverage

DJ Skeletor comes with support for nose test runner and code coverage
reporting through coverage.py.

To run a normal test without code coverage report, run `make test`.

To run a test with a coverage report, run `make coverage`. The report
is generated in HTML format in the `cover/` subdirectory, and in the
Cobertura format in `coverage.xml` file (useful for integrating with
Continuous Integration systems, such as Jenkins). The test run also produces
`nosetests.xml` file in the standard JUnit format, also useful for integration
with Jenkins or other CI systems.

#### Deployments via git

If deployments are done via git (and not fabric, see below), it's
recommended to create another Makefile target that will do the deploy, for
example:

    deploy:
      git pull
      $(MAKE) update
      # command to restart the service(s) as neccessary

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

For all the commands, run 'fab -l' or look at the source.

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

### Renaming the project

By default, DJ Skeletor names the project *project*, so it's generic enough
to not requiring the change for each project, so the initial setup is
a bit faster (and the `manage.py` logic is simpler).

If you do want to change the project name though, there's couple of things
you need to do. For example, if you want to rename the project to *foo*:

* rename the folder: `git mv project foo`
* update `Makefile`, `manage.py` and˛`fabfile` to set `PROJECT_NAME` to `foo`
* commit the changes to your git repository and you're done!

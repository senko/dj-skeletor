# Under which user the application will run; 'vagrant' is the default user on
# Vagrant, so this is the default here. In production, you'll probably want
# to create 'app' user. The user, if missing, is automatically created.
app-user: vagrant
# Where the app will be installed. Vagrant will make the repository root
# directory on the host available as /vagrant/ in the virtual machine, so
# we know we already have the app code available here. In production, you'll
# probably want to set it to /home/<user>/app or similar. If you're pulling
# the code via git (see 'git-repo' below), make sure this directory doesn't
# already exist (or if it does, that it's an already set up git repository
# with the code).
app-root: /vagrant

# On which port will the app server serve the HTTP requests. This is used for
# setting up nginx reverse proxy (nginx will listen on port 80). In production,
app-port: 8000

# Where the Python virtual environment will be created. This is usually
# somewhere in the app user home.
virtualenv-home: /home/vagrant/env

# How many gunicorn workers should be present for Django. It's useful to set
# it to >1 to find race condition bugs before deploying to production.
django-gunicorn-workers: 3

# PostgreSQL database user, password, name and host. If host is "localhost",
# PostgreSQL server and the required user and database will be created locally.
# Otherwise, this is only used as a configuration option for Django.
postgresql-dbuser: app
postgresql-dbpass: app
postgresql-dbname: app
postgresql-dbhost: localhost

# Used only in production: where to pull the source code from. If you're using
# private repositories, you'll probably want to install a known private SSH
# deployment key so you can authenticate with the git repository.
# git-repo: https://github.com/senko/dj-skeletor.git

# Whether to run in development mode or production. In development mode,
# Django will be set up to use dev.py, and gunicorn won't be used. In
# production mode, the prod.py settings will be used and gunicorn will be
# set up to run automatically.
development: True

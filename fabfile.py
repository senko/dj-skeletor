# Common fabric tasks

import os.path
from fabric.api import *
from fabric.contrib.project import rsync_project

def _cd_project_root():
    assert hasattr(env, 'project_path')
    return cd(env.project_path)

def _activate():
    assert hasattr(env, 'virtualenv')
    if '/' in env.virtualenv:
        return prefix('source ' + env.virtualenv + '/bin/activate')
    else:
        return prefix('source ~/.bash_profile 2>/dev/null || ' +
            'source ~/.profile 2>/dev/null || true &&' +
            'workon ' + env.virtualenv)

def _discover_project_name():
    from os import listdir
    from os.path import join, dirname, exists
    project_name = None
    local_root = dirname(__file__)
    for subdir in listdir(local_root):
        if exists(join(local_root, subdir, 'settings', 'test.py')):
            project_name = subdir
            break
    return project_name

# Settings

def env(venv):
    """Virtual environment to use on the server"""
    env.virtualenv = venv

def server(server):
    """Server to use"""
    env.hosts = [server]

def path(path):
    """Project path on the server"""
    env.project_path = path

# Base commands

def rsync():
    """Sync remote files to the server using rsync."""
    assert hasattr(env, 'project_path')
    local_dir = os.path.dirname(__file__) + '/'
    rsync_project(remote_dir=env.project_path, local_dir=local_dir,
        exclude=['media/', 'static/', '*.pyc', '.git/'])

def manage(cmd):
    """Run Django management command on the server"""
    with _activate():
        with _cd_project_root():
            run('python manage.py ' + cmd)

def git_pull(remote='origin'):
    """Pull newest version from the git repository"""
    assert hasattr(env, 'project_path')
    with _cd_project_root():
        run('git pull ' + remote)

def git_clone(origin):
    """Create a new project instance by cloning the source repository"""
    assert hasattr(env, 'project_path')
    run('git clone %s %s' % (origin, env.project_path))

def git_tag_now(prefix):
    """Tag the current branch HEAD with a timestamp"""
    import datetime
    assert hasattr(env, 'project_path')
    with _cd_project_root():
        run('git tag %s-%s' % (prefix,
            datetime.datetime.now().strftime('-%Y-%m-%d-%H-%M-%S')))

# High-level commands

def install_requirements():
    """Install required Python packages (from requirements.txt)"""
    with _activate():
        with _cd_project_root():
            run('pip install -r requirements.txt')

def collectstatic():
    """Collect static files using collectstatic."""
    manage('collectstatic --noinput')

def syncdb():
    """Execute initial syncdb"""
    manage('syncdb')

def migrate():
    """Execute any pending South migrations on the server."""
    manage('migrate')

def test():
    """Run Django tests"""
    assert hasattr(env, 'project_path')
    project_name = _discover_project_name()
    if project_name:
        manage('test --settings=%s.settings.test' % project_name)
    else:
        manage('test')

def update():
    """Do a complete project update.

    This combines:
        - installation of (newly) required Python packages via pip
        - collect new static files
        - upgrade locales,
        - db sync / migrations.
    """
    install_requirements()
    collectstatic()
    syncdb()
    migrate()
    test()

def setup(origin):
    """Create an initial deployment from the source git repository.

    This also sets up a sample settings/local.py which just pulls all
    the settings from dev.py
    """
    assert hasattr(env, 'project_path')
    assert hasattr(env, 'virtualenv')
    git_clone(origin)
    git_tag_now('initial-deploy')
    with prefix('source ~/.bash_profile 2>/dev/null || ' +
            'source ~/.profile 2>/dev/null || true'):
    run('mkvirtualenv --no-site-packages ' + env.virtualenv)
    project_name = _discover_project_name()
    if project_name:
        fname = project_name + '/settings/local.py'
        with _cd_project_root():
            run('test -f %(fname)s || echo "from .dev import *" > %(fname)s' % {
                    'fname': fname
                })
    update()

def deploy():
    """Deploy a new version of the app from the tracked git branch."""
    assert hasattr(env, 'project_path')
    assert hasattr(env, 'virtualenv')
    git_pull()
    git_tag_now('deploy')
    update()

def runserver(host='0.0.0.0', port='8000'):
    """Run a development server on host:port (default 0.0.0.0:8000)"""
    manage('runserver %s:%s' % (host, port))

try:
    from local_fabfile import *
except ImportError:
    pass

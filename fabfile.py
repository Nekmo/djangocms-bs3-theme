# -*- coding: utf-8 -*-
import datetime
import sys

import os
import tempfile

from fabric.api import *
from uuid import uuid4

from fabric.contrib.files import exists

sys.path.append('demo/demo_app')


try:
    from secrets import deploy_settings
except ImportError:
    deploy_settings = None

env.hosts = getattr(deploy_settings, 'hosts', [])
REMOTE_PROJECT = getattr(deploy_settings, 'REMOTE_PROJECT', 'cms-bs3-theme')
COPY_DATABASE = getattr(deploy_settings, 'COPY_DATABASE', False)
DATABASE = getattr(deploy_settings, 'DATABASE', REMOTE_PROJECT)

GIT_PROJECT_URL = 'https://github.com/Nekmo/djangocms-bs3-theme.git'
TEMPDIR = tempfile.tempdir or '/tmp'
MANAGE = 'demo/manage.py'
REMOTE_BACKUPS_DIR = '~/Backups'
STATIC_FILES_DIR = '~/Static'
MAX_DATABASE_BACKUPS = 10
REQUIREMENTS_FILE = 'demo/requirements.txt'
SETTINGS = 'demo_app.settings.production'
MANAGE_PRE_ARGUMENTS = 'PYTHONPATH=::$PWD'
MANAGE_ARGUMENTS = '--settings {} --noinput'.format(SETTINGS)
# http://www.postgresql.org/docs/8.2/static/sql-alterschema.html
CLEAR_SQL = """
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;
COMMENT ON SCHEMA public IS 'standard public schema';
"""
START_VIRTUALENV = 'source `which virtualenvwrapper.sh`; workon {}'.format(REMOTE_PROJECT)


def _nondirty_git():
    lines = local('git status --porcelain', capture=True).stdout.splitlines()
    lines = list(filter(lambda x: not x.startswith('??'), lines))
    if not lines:
        return
    print('Hay cambios pendientes de enviarse en Git:')
    print('\n'.join(lines))
    raise SystemExit()


def _create_project(project):
    project_home = run('echo $PROJECT_HOME').stdout
    if not exists('$PROJECT_HOME/{}'.format(project_home, project)):
        run('mkproject "{}"'.format(project))


def _create_directory(directory):
    if not exists(directory):
        run('mkdir -p {}'.format((directory)))


def _collecstatic():
    static_directory = '{}/{}'.format(STATIC_FILES_DIR, REMOTE_PROJECT)
    _create_directory(static_directory)
    run('{} python {} collectstatic -c {}'.format(MANAGE_PRE_ARGUMENTS, MANAGE, MANAGE_ARGUMENTS))


def _backup_db():
    backup_dir = '{}/{}'.format(REMOTE_BACKUPS_DIR, REMOTE_PROJECT)
    _create_directory(backup_dir)
    run('pg_dump "{}" >> {}/{}'.format(DATABASE, backup_dir,
                                       datetime.datetime.now().replace(microsecond=0).isoformat()))
    # Borrar los archivos más antiguos
    with cd(backup_dir):
        backups_i = int(run('ls -1 | wc -l'.format(REMOTE_BACKUPS_DIR)).stdout)
        if backups_i > MAX_DATABASE_BACKUPS:
            run('rm `ls -1 | head -1`')


def _copy_database():
    dbfile = os.path.join(TEMPDIR, uuid4().hex) + '.dump'
    local('touch "{}"'.format(dbfile))
    local('chmod 600 "{}"'.format(dbfile))
    local('pg_dump "{}" >> {}'.format(DATABASE, dbfile))
    put(dbfile, dbfile, mode="0600")
    local('rm "{}"'.format(dbfile))
    run('psql {} -c "{}"'.format(DATABASE, CLEAR_SQL))
    run('psql "{}" < {}'.format(DATABASE, dbfile))
    # run('rm "{}"'.format(dbfile))


def _migrate():
    run('{} python {} migrate {}'.format(MANAGE_PRE_ARGUMENTS, MANAGE, MANAGE_ARGUMENTS))


def tox():
    if os.path.exists('tox.ini'):
        local('tox')


def deploy(ignore_nondirty=False):
    if not ignore_nondirty:
        _nondirty_git()
    tox()
    _create_project(REMOTE_PROJECT)
    with prefix(START_VIRTUALENV):
        if not exists('.git'):
            run('git clone --recursive {} .'.format(GIT_PROJECT_URL))
        else:
            run('git pull')
        _backup_db()
        run('pip install -r "{}"'.format(REQUIREMENTS_FILE))
        _collecstatic()
    if COPY_DATABASE:
        _copy_database()
    else:
        with prefix(START_VIRTUALENV):
            _migrate()

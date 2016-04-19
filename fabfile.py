import sys

import os
from fabric.api import *

sys.path.append('demo/demo_app')

try:
    from secrets import deploy
except ImportError:
    deploy = None

env.hosts = getattr(deploy, 'hosts', [])


def _nondirty_git():
    lines = local('git status --porcelain', capture=True).stdout.splitlines()
    lines = list(filter(lambda x: not x.startswith('??'), lines))
    if not lines:
        return
    print('Hay cambios pendientes de enviarse en Git:')
    print('\n'.join(lines))
    raise SystemExit()


def tox():
    if os.path.exists('tox.ini'):
        local('tox')


def deploy():
    _nondirty_git()
    tox()
    # run('uname -a')

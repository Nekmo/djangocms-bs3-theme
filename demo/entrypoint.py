#!/usr/bin/env python
import sys

import os

import subprocess


COMMIT_FILE = '.last_build_commit'
os.environ.setdefault('BUILD_DJANGO', '1')
os.environ.setdefault('FORCE_BUILD', '1')


def execute_command(*args):
    subprocess.check_call(args)


def get_current_commit():
    return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('utf-8').strip()


def read_file():
    if not os.path.lexists(COMMIT_FILE):
        return ''
    with open(COMMIT_FILE, 'r') as f:
        return f.read().strip('\n')


def write_file(data):
    if data is None:
        return
    with open(COMMIT_FILE, 'w') as f:
        return f.write(data)


def build_now():
    execute_command('make', 'collectstatic')
    # execute_command('./manage.py', 'collectstatic', '--noinput')
    execute_command('make', 'migrate')


def build(force_build=False):
    current_commit = None
    if not force_build:
        current_commit = get_current_commit()
    if force_build or read_file() != current_commit:
        try:
            build_now()
        except subprocess.CalledProcessError:
            exit(1)
        else:
            write_file(current_commit)


def start(*parameters):
    subprocess.check_call(['gunicorn'] + list(parameters))


if __name__ == '__main__':
    if os.environ.get('BUILD_DJANGO') == '1':
        build(os.environ.get('FORCE_BUILD') == '1')
    start(*sys.argv[1:])

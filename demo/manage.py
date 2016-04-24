#!/usr/bin/env python
import os
import sys


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


try:
    import cms_bs3_theme
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(BASE_DIR, '../')))


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo_app.settings.defaults")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

"""
WSGI config for djangocms-bs3-theme project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    import cms_bs3_theme
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(BASE_DIR, '../../')))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo_app.settings.production")

application = get_wsgi_application()

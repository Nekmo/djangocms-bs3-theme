from .defaults import *

SECRET_KEY = getattr(secrets, 'SECRET_KEY', SECRET_KEY)
DATABASES = getattr(secrets, 'DATABASES', DATABASES)

DEBUG = False
ALLOWED_HOSTS = ['*']
STATIC_ROOT = os.path.expanduser('~/Static')
from .defaults import *

SECRET_KEY = os.environ.get('SECRET_KEY')

DATABASES = {
    'default': {
        'CONN_MAX_AGE': 0,
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'demo_postgres_1',
        'NAME': os.getenv("POSTGRES_DB"),
        'USER': os.getenv("POSTGRES_USER"),
        'PASSWORD': os.getenv("POSTGRES_PASSWORD"),
        'PORT': '',
    }
}

DEBUG = False
ALLOWED_HOSTS = ['*']
STATIC_ROOT = '/static'

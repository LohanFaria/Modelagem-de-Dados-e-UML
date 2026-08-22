import os
from decouple import config, Csv
from .base import *

DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1,0.0.0.0', cast=Csv())

import sys

# Database configuration (PostgreSQL por padrão, SQLite durante testes locais ou se DB_ENGINE=sqlite)
DB_ENGINE = config(
    'DB_ENGINE',
    default='sqlite' if ('pytest' in sys.modules or 'pytest' in sys.argv[0]) else 'django.db.backends.postgresql'
)

if DB_ENGINE == 'sqlite':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default='xpto'),
            'USER': config('DB_USER', default='xpto'),
            'PASSWORD': config('DB_PASSWORD', default='xpto_password_secret'),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }

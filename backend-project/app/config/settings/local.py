from .base import *

SECRET = json.load(open(os.path.join(SECRET_ROOT, 'local_database.json')))

DEBUG = True

INSTALLED_APPS += [
    'debug_toolbar',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'PORT': 5432,
        'USER': SECRET['USER'],
        'PASSWORD': SECRET['PASSWORD'],
        'NAME': SECRET['NAME']
    }
}

# debug toolbar setting
INTERNAL_IPS = ('127.0.0.1',)

WSGI_APPLICATION = 'config.wsgi.local.application'

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

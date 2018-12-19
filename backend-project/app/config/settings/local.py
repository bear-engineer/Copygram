from .base import *

SECRET = json.load(open(os.path.join(SECRET_ROOT,'local_database.json')))

DEBUG = True

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'PORT': 5432,
            'USER': SECRET['USER'],
            'PASSWORD': SECRET['PASSWORD'],
            'NAME': SECRET['NAME']
        }
    }

WSGI_APPLICATION = 'config.wsgi.local.application'
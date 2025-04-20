from luxury_reservations_bk.settings import *
import os

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'rdsejemplo',
        'USER': "postgres",
        'PASSWORD': 'KFmDKUVCgX',
        'HOST': 'rds-ejemplo.cdw4cq0g8nab.us-east-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

FONT_PATH = os.path.join(BASE_DIR, "static",'fonts')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
URLPAGE = 'http://localhost:5174'

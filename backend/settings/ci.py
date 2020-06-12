from .base import *

DEBUG = False

SECRET_KEY = 'azyr8U@S9GqFwdY79t^Edlwb#Q@7'
TOKEN_EXPIRED_AFTER_SECONDS = 86400

DEFAULT_FROM_EMAIL = 'example@gmail.com'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'mysql',
        'USER': 'root',
        'PASSWORD': '12345678',
        'NAME': 'ci_test'
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
UPLOAD_FILE_DIR = os.path.join(BASE_DIR, 'media')
MOMO_SECRET_KEY = 'secret'
DJANGO_HOST = '127.0.0.1'
VUE_HOST = '127.0.0.1'
PARTNER_CODE = 'partner_code'
MOMO_ACCESS_KEY = 'access_key'

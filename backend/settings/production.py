from .base import *

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')
TOKEN_EXPIRED_AFTER_SECONDS = int(os.environ.get('TOKEN_EXPIRED_AFTER_SECONDS'))
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')

ALLOWED_HOSTS = [os.environ.get('HOST_IP')]

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE'),
        'HOST': os.environ.get('DB_HOST'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'NAME': os.environ.get('DB_NAME')
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

UPLOAD_FILE_DIR = os.environ.get('UPLOAD_FILE_DIR')

AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
AWS_ACCESS_TOKEN = os.environ.get('AWS_ACCESS_TOKEN')
AWS_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')

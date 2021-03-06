import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTH_USER_MODEL = 'users.User'

ROOT_URLCONF = 'urls'
WSGI_APPLICATION = 'wsgi.application'

EMAIL_USE_LTS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
ENAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
USE_L10N = True
USE_TZ = True
APP_NAME = 'rest boilerplate'
DEBUG = False
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'safedelete',
    'corsheaders',

    'users',
    'auth_tokens',
    'clients',
    'folders',
    'templates',
    'bounding_boxes',
    'tasks',
    'images',
    'results',
    'bills'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'auth_tokens.services.ExpiringTokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'EXCEPTION_HANDLER': 'utils.exception_handler.custom_exception_handler',
    'UNAUTHENTICATED_USER': None
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [os.path.join(BASE_DIR, 'utils/templates'), ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

IMAGE_TYPES = ['.jpg', '.jpeg', '.png', '.bmp', '.eps', '.raw', '.tif', '.tiff']

FIXTURE_DIRS = [
    os.path.join(BASE_DIR, 'utils', 'fixtures')
]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

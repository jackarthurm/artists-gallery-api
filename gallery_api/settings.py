"""
Django settings for gallery_api project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

import dj_database_url
from django.core.exceptions import ImproperlyConfigured


# Allows running management commands without defining all env vars. Must be
# set to True in production
THROW_FOR_MISSING_ENV_VARS: bool = True


def get_env_var(key: str):

    try:
        return os.environ[key]
    except KeyError:

        if THROW_FOR_MISSING_ENV_VARS:
            raise ImproperlyConfigured(
                f'Missing environment variable {key}'
            )

        return ''


def get_env_var_bool(key: str):
    return get_env_var(key).upper() == 'TRUE'


def get_env_var_list(key: str):
    return get_env_var(key).split()


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


SECRET_KEY = get_env_var('SECRET_KEY')

DEBUG = get_env_var_bool('DEBUG')

ALLOWED_HOSTS = get_env_var_list('ALLOWED_HOSTS')


# CORS
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = get_env_var_list('CORS_ORIGIN_WHITELIST')

CORS_URLS_REGEX = r'^/api/.*$'
CORS_ALLOW_METHODS = (
    'GET',
    'OPTIONS'
)
CORS_ALLOW_HEADERS = (
    'content-type',
    'accept'
)
CORS_EXPOSE_HEADERS = (
    'Access-Control-Allow-Origin: *',
)


# Application definition
INSTALLED_APPS = [
    'gallery_api.apps.GalleryAPIAdminConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'image_api',
    'email_api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gallery_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
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

WSGI_APPLICATION = 'gallery_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': dj_database_url.config(conn_max_age=600)
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilari'
                'tyValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidato'
                'r',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidat'
                'or',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValida'
                'tor',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_L10N = True
USE_TZ = True


REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPaginatio'
                                'n',
    'PAGE_SIZE': 100,
    'DEFAULT_THROTTLE_CLASSES': (
        'gallery_api.throttles.AnonBurstRateThrottle',
        'gallery_api.throttles.AnonSustainedRateThrottle',
        'rest_framework.throttling.ScopedRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'burst': '60/min',
        'sustained': '10000/day',
        'contact': '10/hour',
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = DEFAULT_FILE_STORAGE

AWS_DEFAULT_ACL = 'public-read'
AWS_ACCESS_KEY_ID = get_env_var('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_env_var('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = get_env_var('AWS_STORAGE_BUCKET_NAME')
AWS_AUTO_CREATE_BUCKET = False
AWS_QUERYSTRING_AUTH = False
AWS_QUERYSTRING_EXPIRE = None
AWS_S3_ENCRYPTION = False
AWS_S3_FILE_OVERWRITE = True
AWS_S3_REGION_NAME = get_env_var('AWS_S3_REGION_NAME')
AWS_S3_USE_SSL = get_env_var_bool('AWS_S3_USE_SSL')


# Admin site
SITE_NAME = get_env_var('SITE_NAME')
DJANGO_ADMIN_SITE_HEADER = f'{SITE_NAME} admin'
DJANGO_ADMIN_SITE_TITLE = f'{SITE_NAME} admin portal'
DJANGO_ADMIN_SITE_INDEX_TITLE = f'{SITE_NAME} admin portal'
DJANGO_ADMIN_SITE_LINK_URL = get_env_var('FRONTEND_URL')


# Email config
CONTACT_EMAILS = get_env_var_list('CONTACT_EMAILS')
DEFAULT_FROM_EMAIL = get_env_var('DEFAULT_FROM_EMAIL')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = get_env_var_bool('EMAIL_USE_TLS')
EMAIL_HOST = get_env_var('EMAIL_HOST')
EMAIL_PORT = get_env_var('EMAIL_PORT')
EMAIL_HOST_USER = get_env_var('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_env_var('EMAIL_HOST_PASSWORD')
EMAIL_SUBJECT = f'New contact at {SITE_NAME}'

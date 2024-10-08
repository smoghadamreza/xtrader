"""
Django settings for xtrader project.

Generated by 'django-admin startproject' using Django 1.10.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""
# import asgi_redis
import os
from django.conf import settings
import sys
import time
import threading
from pathlib import Path

settings_dir = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = Path(__file__).resolve().parent.parent
# TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'mytemplates'),
#                  os.path.join(PROJECT_ROOT, 'templates/'),)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get('DEBUG', 1)))

ALLOWED_HOSTS = []
ALLOWED_HOSTS.extend(
    filter(
        None,
        os.environ.get('ALLOWED_HOSTS', '').split(','),
    )
)
# Settings used by Userena
LOGIN_REDIRECT_URL = "/accounts/%(username)s/"
LOGIN_URL = "/accounts/signin/"
LOGOUT_URL = "/accounts/signout/"
AUTH_PROFILE_MODULE = 'accounts.Profile'
USERENA_DISABLE_PROFILE_LIST = True
USERENA_MUGSHOT_SIZE = 140



USERENA_REDIRECT_ON_SIGNOUT = getattr(settings,
                                      'USERENA_REDIRECT_ON_SIGNOUT',
                                      '/accounts/signin')
USERENA_SIGNIN_REDIRECT_URL = getattr(settings,
                                      'USERENA_SIGNIN_REDIRECT_URL',
                                      '/robots')
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # 'mabna',
    # 'show',
    # 'api',
    'accounts',
    # 'chat',
    'main',
    'django.contrib.sites',
    'finance',
    'data',
    'sales',
    'userena',
    'guardian',
    'easy_thumbnails',
    'channels',
    'social',
    'bootstrap3',
    'aum',
]
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "asgi_redis.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379')],
#         },
#         "ROUTING": "chat.routing.channel_routing",
#     },
# }
SITE_ID = 1
REDIS_DB = 0
# settings.py
INTERVALS = [1, 5, 10, 30, 60]  # Example list of intervals
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'xtrader.urls'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_PORT = 587
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]
WSGI_APPLICATION = 'xtrader.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DB_HOST'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
        'PORT': '5432',
    }
}
USE_TZ = True
TIME_ZONE = 'Iran'
# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

# LANGUAGE_CODE = 'fa-ir'

USE_I18N = True

USE_L10N = True
AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
# PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
# STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
#STATICFILES_DIRS = (
#    os.path.join(BASE_DIR, 'static'),
#)
MEDIA_ROOT = '/vol/web/media'
STATIC_ROOT = '/vol/web/static'
#MEDIA_URL = 'media/'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
XTREASURY_BOT = ''
USDT_WALLET = ''
REFERRAL_BOUNCE = .3
ADMIN_TEL_ID = 121366977
COPYTRADEFEE = 0.4
# from django.utils.translation import ugettext_lazy as _

# LANGUAGES = (
#     ('en', _('English')),
#     ('fa', _('Farsi')),
# )
LOG_LEVEL = 'INFO'
try:
    from .localsetting import *
except ImportError:
    pass

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        # 'file': {
        #     'level': 'ERROR',
        #     'class': 'logging.FileHandler',
        #     'filename': 'errors.log',
        # },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
    },
}

ANONYMOUS_USER_NAME = "AnonymousUser"
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

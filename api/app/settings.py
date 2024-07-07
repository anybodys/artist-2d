"""
Django settings for API project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


ENV = os.environ["ENV"]
IS_PROD = ENV == "prod"
PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", None)
REGION = os.environ.get("GOOGLE_CLOUD_REGION", "us-west1")
SECRET_KEY = os.environ["SECRET_KEY"]
SECRET_KEY_FALLBACKS = [
  # Put old secret keys here when rotating. Remove promptly!
]

DEBUG = not IS_PROD

CLOUDRUN_SERVICE_URL = os.environ.get("CLOUDRUN_SERVICE_URL", default=None)
if CLOUDRUN_SERVICE_URL:
  ALLOWED_HOSTS = [urlparse(CLOUDRUN_SERVICE_URL).netloc]
  CSRF_TRUSTED_ORIGINS = [CLOUDRUN_SERVICE_URL]
  SECURE_SSL_REDIRECT = True
  SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
else:
  #assert not IS_PROD
  ALLOWED_HOSTS = ["*"]


CORS_ALLOWED_ORIGINS = [
  # Prod
  "https://kmdcodes.com",
  # Local
  "http://localhost:3000",
  "http://127.0.0.1:3000",
]
CORS_ALLOW_CREDENTIALS = True


# Application definition

INSTALLED_APPS = [
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',

  'corsheaders',
  'api',

  'allauth',
  'allauth.account',
  'allauth.socialaccount',
  'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'corsheaders.middleware.CorsMiddleware',
  'django.middleware.common.CommonMiddleware',
  #'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',

  'allauth.account.middleware.AccountMiddleware',

  #'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

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

WSGI_APPLICATION = 'app.wsgi.application'


DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': os.environ.get("POSTGRES_DB", "artist"),
    "HOST": os.environ.get("POSTGRES_HOST", "db"),
    "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    "USER": os.environ['POSTGRES_USER'],
    "PASSWORD": os.environ['POSTGRES_PASSWORD'],
  }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Social Auth with allauth

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
  'google': {
    # For each OAuth based provider, either add a ``SocialApp``
    # (``socialaccount`` app) containing the required client
    # credentials, or list them here:
    'APP': {
      'client_id': os.environ['GOOGLE_OAUTH2_KEY'],
      'secret': os.environ['GOOGLE_OAUTH2_SECRET'],
      'key': '',
    },
    'SCOPE': [
      'profile',
      'email',
    ],
    'AUTH_PARAMS': {
      'access_type': 'online',
    },
  },
}

SOCIALACCOUNT_ONLY = True
ACCOUNT_EMAIL_VERIFICATION = 'none'

if IS_PROD:
  ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

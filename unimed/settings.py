"""
Django settings for unimed project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'r15j)s2)8+k&1_9p9gaz^gf-olp-)v)57hd_dl__t)ki^h%f_0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'core',
    'website',
    'telegram_bot',
    'webbot',
    'rest_framework',
    'api.apps.ApiConfig',
    'corsheaders',
]

CORS_ORIGIN_ALLOW_ALL=True

CORS_ORIGIN_WHITELIST = [
    'http://google.com',
    'http://hostname.example.com',
    'http://localhost:8000',
    'http://127.0.0.1:9000',
    
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

ROOT_URLCONF = 'unimed.urls'
DEFAULT_AUTO_FIELD='django.db.models.AutoField'
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



WSGI_APPLICATION = 'unimed.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# if PRODUCTION_MODE:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql',
#             'NAME': os.environ['POSTGRES_DB'],
#             'USER': os.environ['POSTGRES_USER'],
#             'PASSWORD': os.environ['POSTGRES_PASSWORD'],
#             'HOST': os.environ['POSTGRES_HOST'],
#             'PORT': os.environ['POSTGRES_PORT'],
#         }
#     }
# else:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

GROUP_ID = '-592583437'
MAIN_URL = 'https://unimedtrade.uz'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

LOC = 41.332717
LOC1 = 69.288738


# TOKEN = '1865681910:AAGhE98ZwhXcbUAfrGE0iXrt0Vp_8ZcHB5I' #test
# # https://api.telegram.org/bot1865681910:AAGhE98ZwhXcbUAfrGE0iXrt0Vp_8ZcHB5I/setWebhook?url=https://06275081b466.ngrok.io/telegram/1865681910:AAGhE98ZwhXcbUAfrGE0iXrt0Vp_8ZcHB5I/

TOKEN = '1835181022:AAEui83kmGrfEjQ52Lg2xXwpDW1fJU-dQi0' # prod
# https://api.telegram.org/bot1835181022:AAEui83kmGrfEjQ52Lg2xXwpDW1fJU-dQi0/setWebhook?url=https://unimedtrade.uz/telegram/1835181022:AAEui83kmGrfEjQ52Lg2xXwpDW1fJU-dQi0/


CRISPY_TEMPLATE_PACK = 'bootstrap4'

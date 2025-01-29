"""
Django settings for e_learn project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from .info import * 
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "learn/static",
]

MEDIA_URL = '/media/' #-> http://127.0.0.1:8000/media (handles urls served from MEDIA_ROOT)
MEDIA_ROOT = BASE_DIR / "media" #-> Abs path to media folder
# Add root to Project urls.py  

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
ENVIRONMENT = ENVIRONMENT
if ENVIRONMENT == 'production':
    DEBUG = False   
else:
    DEBUG = True

ALLOWED_HOSTS = ['*']

SESSION_ENGINE = 'django.contrib.sessions.backends.db' 
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = EMAIL_USE_TLS
EMAIL_HOST = EMAIL_HOST
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
EMAIL_PORT = EMAIL_PORT


# Site information
SITE_INFO = {
    "description": "Hello, this project uses Django and Vanilla HTML and CSS, bootstrap, and jQuery. \
                    The UI was collected from FreeCSS.com and HTML5 Boilerplate. \
                    The website is about buying online courses and videos about online learning. \
                    The goal of this project is to create an online learning platform for anyone.",
    "address": "Mirpur , Dhaka, Bangladesh",
    "email": "111raihanrony111@gmail.com",
    "phone": "+1234567890",
    "social_links": {
        "facebook": "https://facebook.com/profile.php?id=61571444717820",
        "twitter": "https://twitter.com/",
        "linkedin": "https://www.linkedin.com/in/raihan-rony-a461121a1/",
        "instagram": "https://instagram.com/",
        "youtube": "https://youtube.com/",
    },
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'learn',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'e_learn.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "learn/templates/learn",
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'learn.context_processors.site_info',
            ],
        },
    },
]

WSGI_APPLICATION = 'e_learn.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "e_learn",
        "HOST": "127.0.0.1",
        "PORT": "3306",
        "USER": MYSQL_USER,
        "PASSWORD": MYSQL_PASSWORD,
    }
}

POSTGRE_LOCALLY = config('POSTGRE_LOCALLY')

if POSTGRE_LOCALLY:
    DATABASES['default'] = dj_database_url.parse(config('DATABASE_URL'))

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_TZ = True
TIME_ZONE = "Asia/Dacca"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_URL = 'learn:login'
LOGOUT_REDIRECT_URL = 'learn:home'

ACCOUNT_USERNAME_BLACKLIST = ['account','accounts','admin','admins', 'category', 
                            'post', 'inbox', 'profile', 'signup', 'signin', 'signout', 'sign in', 
                            'sign up', 'sign out', 'sign-in', 'sign-up', 'sign-out', 'boss']
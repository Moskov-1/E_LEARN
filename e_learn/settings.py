
import os
from pathlib import Path
from .info import * 
import dj_database_url
from decouple import config
import cloudinary
import cloudinary.uploader
import cloudinary.api

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = EMAIL_USE_TLS
EMAIL_HOST = EMAIL_HOST
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
EMAIL_PORT = EMAIL_PORT
WSGI_APPLICATION = 'e_learn.wsgi.application'
ROOT_URLCONF = 'e_learn.urls'


LOGIN_URL = 'learn:login'
LOGOUT_REDIRECT_URL = 'learn:home'
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


BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_URL = 'static/'
MEDIA_URL = 'media/'

ENVIRONMENT = config('ENVIRONMENT', default='development')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
if ENVIRONMENT == 'production':
    DEBUG = False
else:
    DEBUG = True
    
if ENVIRONMENT == 'production':    # Tell Django to copy static assets into a path called `staticfiles` (this is specific to Render)
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    'learn',
]

CLOUDINARY_STORAGE = {
    "CLOUD_NAME" : config('CLOUD_NAME'), 
    "API_KEY" : config('CLOUD_API_KEY'), 
    "API_SECRET" : config('CLOUD_API_SECRET'), 
}
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
cloudinary.config( 
    cloud_name = config('CLOUD_NAME'), 
    api_key = config('CLOUD_API_KEY'), 
    api_secret = config('CLOUD_API_SECRET'), 
    secure=True,
)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / "learn/templates/learn",],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'learn.context_processors.site_info',
                'learn.context_processors.tag_context_processor',
            ],
        },
    },
]


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

if ENVIRONMENT == 'production':
    DATABASES['default'] = dj_database_url.parse(config('DATABASE_URL'))

# Password validation
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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

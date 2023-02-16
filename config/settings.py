from pathlib import Path
from decouple import config
import redis
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='fjkg4875556-fgf567-/%yh&&@#!bgh9jtf')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=lambda v:bool(int(v)), default=True)

def parse_list_cast(value):
    if type(value) == str:
        return [i.strip() for i in value.split()]
    elif type(value) in [list, tuple]:
        return [i.strip() for i in value]
    else:
        return value
    
ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    cast=parse_list_cast,
    default=["*"]
)

INTERNAL_IPS = config(
    "INTERNAL_IPS",
    cast=parse_list_cast,
    default=["*"]
)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party apps
    'rest_framework',
    'django_filters',
    'drf_yasg',
    'django_cleanup.apps.CleanupConfig',
    'phonenumber_field',
    'rest_framework_simplejwt',
    # Project apps
    'account.apps.AccountConfig',
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

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": config("DB_ENGINE", default="django.db.backends.postgresql"),
        "NAME": config("DB_NAME", default="online_store"),
        "USER": config("DB_USER", default="online_store"),
        "PASSWORD": config("DB_PASSWORD", default="online_store"),
        "HOST": config("DB_HOST", default="postgres"),
        "PORT": config("DB_PORT", default=5432),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Redis
REDIS_HOST = config("REDIS_HOST", default="redis")
REDIS_PORT = config("REDIS_PORT", default=6379)
REDIS_DB_NUMBER = config("REDIS_DB_NUMBER", default=0)

redis_connection = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_NUMBER)

# Cache FrameWork Config
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_NUMBER}",
    }
}

# Phone number field config
PHONENUMBER_DB_FORMAT = "NATIONAL"
PHONENUMBER_DEFAULT_FORMAT = "NATIONAL"
PHONENUMBER_DEFAULT_REGION = 'IR'

# One-time code config
CODE_EXPIRE_TIME = 3 # minutes 
CODE_LENGTH = 6 # max:20

# User model
AUTH_USER_MODEL = 'account.User'

# URL
PROJECT_HOST = "127.0.0.1"
if DEBUG:
    PROJECT_PORT = "8000"
else:
    PROJECT_PORT = "80"  
PROJECT_SCHEMA = "http" 

# DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS':(
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter'
    ),
    'DEFAULT_PAGINATION_CLASS':'common.paginations.DefaultPagination'
}

# Simple JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=24),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=60),
    "AUTH_HEADER_TYPES": ("Bearer", "jwt", "JWT",),
}

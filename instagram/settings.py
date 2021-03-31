"""
Django settings for instagram project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from datetime import timedelta
from pathlib import Path
import environ

env = environ.Env(
    # set casting, default value. Ex: DJANGO_DEBUG=(bool, True),
    ENVIRONMENT=(str, 'development'),
    DEBUG=(bool, True),
    SECRET_KEY=(str, r'h#(pb@2_)viux4ze8wqit=j6di@1jly6_s4zte5dm4bh9jv7yl'),
    DATABASE_URL=(str, r'sqlite://../db.sqlite3'),
    LANGUAGE_CODE=(str, 'vi'),
    ACTIVATE_JWT=(bool, False),
    SOCIAL_AUTH_FACEBOOK_KEY=(str, ''),
    SOCIAL_AUTH_FACEBOOK_SECRET=(str, ''),
    FB_ACCESS_TOKEN=(str, ''),
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=(str, ''),
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=(str, ''),
    AWS_ACCESS_KEY_ID=(str, ''),
    AWS_SECRET_ACCESS_KEY=(str, ''),
    AWS_STORAGE_BUCKET_NAME=(str, ''),
    DEFAULT_FILE_STORAGE=(str, 'django.core.files.storage.FileSystemStorage'),
    STATICFILES_STORAGE=(str, 'whitenoise.storage.CompressedManifestStaticFilesStorage')
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env.read_env(env.str('ENV_PATH', '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'users.apps.UsersConfig',
    'posts.apps.PostsConfig',
    'images.apps.ImagesConfig',
    'comments.apps.CommentsConfig',
    'likes.apps.LikesConfig',

    'django_extensions',
    'oauth2_provider',
    'social_django',
    'drf_social_oauth2',
    'debug_toolbar',
    'django_cleanup.apps.CleanupConfig',
    'django_filters',
]

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',
    # 'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ...
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # ...
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # ...
    'request_logging.middleware.LoggingMiddleware',
]

ROOT_URLCONF = 'instagram.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'instagram.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    # read os.environ['DATABASE_URL'] and raises ImproperlyConfigured exception if not found
    'default': env.db('DATABASE_URL'),
    # read os.environ['SQLITE_URL']
    # 'extra': env.db('SQLITE_URL', default='sqlite:////tmp/my-tmp-sqlite.db')
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = env('LANGUAGE_CODE')

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'drf_social_oauth2.authentication.SocialAuthentication',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

AUTHENTICATION_BACKENDS = (

    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.facebook.FacebookAppOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'drf_social_oauth2.backends.DjangoOAuth2',
    'social_core.backends.google.GoogleOAuth2'
)

# Facebook configuration
SOCIAL_AUTH_FACEBOOK_KEY = env('SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = env('SOCIAL_AUTH_FACEBOOK_SECRET')
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id, name, email'
}

# Google configuration
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

# Define SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE to get extra permissions from Google.
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]

ACTIVATE_JWT = env('ACTIVATE_JWT')

AUTH_USER_MODEL = 'users.User'

MEDIA_ROOT = environ.os.path.join(BASE_DIR, 'media')
print(MEDIA_ROOT)
MEDIA_URL = '/media/'  # 'http://myhost:port/media/'

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=7),
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'sqlformatter': {
            '()': 'ddquery.SqlFormatter',
            'format': '%(levelname)s %(message)s',
            'highlight': True
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'handlers': {
        'console-db': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'sqlformatter',
        },
        'console': {
            'level': 'DEBUG',
            'filters': [],
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console-db'],
        },
        'django.server': {
            'level': 'DEBUG',
            'handlers': ['console']
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',  # change debug level as appropiate
            'propagate': False,
        },
    }
}

INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]


DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda r: DEBUG,  # disables it
    # '...
}
STATIC_URL = '/static/'
STATIC_ROOT = environ.os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = env('STATICFILES_STORAGE')
DEFAULT_FILE_STORAGE = env('DEFAULT_FILE_STORAGE')

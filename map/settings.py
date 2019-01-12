"""
Django settings for map project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import os.path
from django.conf.global_settings import LOGIN_REDIRECT_URL
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGIN_REDIRECT_URL = '/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nipn@lh_e2+_gsw$u5u=bs0^-kiry0cqr*1^#emsfi31vdb$c7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Application definition

INSTALLED_APPS = [
    'grappelli',
    'django.contrib.gis',
    'django.contrib.admin',
    "compressor",
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'leaflet',
    'djgeojson',
    'guardian',
    'map'
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # this is default
    'guardian.backends.ObjectPermissionBackend',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'map.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'map.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'fsfehpjo',
        'USER': 'fsfehpjo',
        'PASSWORD': 'GnQ30PDygIRCq3t7tQVoreA4vinWjSdg',
        'HOST': 'packy.db.elephantsql.com',
        'PORT': '',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

GDAL_LIBRARY_PATH = os.environ.get('GDAL_LIBRARY_PATH')

GEOS_LIBRARY_PATH = os.environ.get('GEOS_LIBRARY_PATH')

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')

STATIC_URL = '/static/'

STATICFILES_DIRS = os.path.join(PROJECT_ROOT, 'staticfiles')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_JS_FILTERS = [
    'compressor.filters.template.TemplateFilter',
]

COMPRESS_ENABLED = False

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '127.0.0.1:6379',
    },
}


LEAFLET_CONFIG = {
    #'TILES':'https://2.base.maps.api.here.com/maptile/2.1/mapnopttile/newest/normal.day/{z}/{x}/{y}/256/png8?app_id=xFlVyCWdTcCybguLGWAb&app_code=HEoHoQb3yk39kcOKN2RH_w',
    #'TILES':'https://2.aerial.maps.api.here.com/maptile/2.1/maptile/newest/hybrid.day/{z}/{x}/{y}/256/png8?app_id=xFlVyCWdTcCybguLGWAb&app_code=HEoHoQb3yk39kcOKN2RH_w',
    'TILES': [('Normal & Hi-res', 'https://2.base.maps.api.here.com/maptile/2.1/mapnopttile/newest/normal.day/{z}/{x}/{y}/512/png8?style=fleet&app_id=xFlVyCWdTcCybguLGWAb&app_code=HEoHoQb3yk39kcOKN2RH_w&ppi=320', {'attribution': ''}),
            ('Satellite & Transport', 'https://2.aerial.maps.api.here.com/maptile/2.1/maptile/newest/hybrid.day/{z}/{x}/{y}/256/png8?app_id=xFlVyCWdTcCybguLGWAb&app_code=HEoHoQb3yk39kcOKN2RH_w', {'attribution': ''})],
    'ATTRIBUTION_PREFIX': 'by imgVOID',
    'DEFAULT_CENTER': (50.4501, 30.5234),
    'DEFAULT_ZOOM': 15,
    'MIN_ZOOM': 12,
    'MAX_ZOOM': 18,
    'RESET_VIEW' : False,
    #'FORCE_IMAGE_PATH': True,
    'PLUGINS': {
        'fullscreen': {
            'css': 'css/fullscreen.css',
            'js': 'js/fullscreen.js',
            'auto-include': True,
        },
        'buttons': {
            'css': 'css/easy-button.css',
            'js': 'js/easy-button.js',
            'auto-include': True,
        },
        'sidebar': {
            'css': 'css/L.Control.Sidebar.css',
            'js': 'js/L.Control.Sidebar.js',
            'auto-include': True,
        },
        'routing': {
            'css': 'css/routing.css',
            'js': 'js/routing.js',
            'auto-include': True,
        },
    }
}

GRAPPELLI_ADMIN_TITLE = 'CityQuest'

# Activate Django-Heroku.
django_heroku.settings(locals())

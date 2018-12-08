"""
Django settings for map project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
from django.conf.global_settings import LOGIN_REDIRECT_URL

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
    'django.contrib.admin',
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

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    # ... another middlewares
    'django.middleware.common.CommonMiddleware',
    # ... rest of middlewares
    'django.middleware.cache.FetchFromCacheMiddleware',
]

ROOT_URLCONF = 'map.urls'

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

WSGI_APPLICATION = 'map.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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

STATIC_URL = '/static/'

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
    'PLUGINS': {
        'fullscreen': {
            'css': 'https://api.mapbox.com/mapbox.js/plugins/leaflet-fullscreen/v1.0.1/leaflet.fullscreen.css',
            'js': 'https://api.mapbox.com/mapbox.js/plugins/leaflet-fullscreen/v1.0.1/Leaflet.fullscreen.min.js',
            'auto-include': True,
        },
        'buttons': {
            'css': 'https://cdn.jsdelivr.net/npm/leaflet-easybutton@2/src/easy-button.css',
            'js': 'https://cdn.jsdelivr.net/npm/leaflet-easybutton@2/src/easy-button.js',
            'auto-include': True,
        },
        'sidebar': {
            'css': '/map/static/css/L.Control.Sidebar.css',
            'js': '/map/static/js/L.Control.Sidebar.js',
            'auto-include': True,
        },
        'routing': {
            'css': 'https://unpkg.com/leaflet-routing-machine@latest/dist/leaflet-routing-machine.css',
            'js': 'https://unpkg.com/leaflet-routing-machine@latest/dist/leaflet-routing-machine.js',
            'auto-include': True,
        },
    }
}
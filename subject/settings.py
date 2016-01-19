import os
from django.conf.global_settings import MEDIA_URL
BASE_DIR = os.path.dirname(os.path.dirname(__file__),)
SECRET_KEY = '1+z60-pf0mz6_7ofaahfa*u_g7a95f(68r&1s-3#_+%0cymr_g'

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'exercise',
    'login',
    'collection',
    'activity',
    'resources',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'subject.urls'

WSGI_APPLICATION = 'subject.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'subject',
        'USER': 'root',
        'PASSWORD': 'warmer',
        'HOST': '',
        'PORT': '',
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATICFILES_DIRS = (  
    'static',  
)  
STATIC_ROOT = os.path.join(BASE_DIR,'subject/static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/').replace("\\","/")


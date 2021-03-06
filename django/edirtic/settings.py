"""
Django settings for edirtic project.
"""

from os.path import abspath, dirname, join

PROJECT = "edirtic"
PROJECT_VERBOSE = "Main Courante edirTIC31"

BASE_DIR = dirname(dirname(abspath(__file__)))
SECRET_KEY = '11+)$2+ulb9nn)x4(g4wedajo4=!olbn%_d8ebqo!xw(j!r8&1'
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    PROJECT,
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tastypie',
    'bootstrap3',
    'djangobower',
    'accounts',
    'maincourante',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'maincourante.middleware.EvenementMiddleware',
]

ROOT_URLCONF = '%s.urls' % PROJECT

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
                'maincourante.context_processors.evenement',
            ],
        },
    },
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
)

WSGI_APPLICATION = '%s.wsgi.application' % PROJECT

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(BASE_DIR, 'db.sqlite3'),
    }
}

BOWER_COMPONENTS_ROOT = join(BASE_DIR, 'components')

BOWER_INSTALLED_APPS = (
    'bootstrap',
    'jquery',
    'angular',
    'angular-animate',
    'angular-bootstrap',
    'angular-resource',
    'angular-route',
    'angucomplete-alt',
    'ng-focus-on',
)

LANGUAGE_CODE = 'fr-FR'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

USE_L10N = False
DATETIME_FORMAT = "d b Y à H:i:s"

STATIC_URL = '/static/'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'list-evenements'

ANGULAR = False

BOOTSTRAP3 = {
    'jquery_url': STATIC_URL + 'jquery/dist/jquery.js',
    'base_url': STATIC_URL + 'bootstrap/dist/',
    'horizontal_label_class': 'col-md-3',
    'horizontal_field_class': 'col-md-6',
}

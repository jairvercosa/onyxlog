import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = 'iczggaeda^c-kf!t4e0gotd8i^ts0a+_sy=_s7r$^ucu&o3yuv'

DEBUG = False
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '10.10.2.132', 'onyxlog.totvs.com.br', '187.94.58.26']

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap_toolkit',
    'django_bootstrap_breadcrumbs',
    'south',
    'onyxlog.core',
    'onyxlog.acesso',
    'onyxlog.cliente',
    'onyxlog.equipe',
    'onyxlog.oportunidade',
    'onyxlog.relatorio',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'onyxlog.urls'
WSGI_APPLICATION = 'onyxlog.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tsmtestdb',                     
        'USER': 'tsmdb_user',
        'PASSWORD': 'G85dXJO1Q72101G',
        'HOST': 'localhost',
        'PORT': '3306',                     
        'HOST': '/var/lib/mysql/mysql.sock',
    }
}
SOUTH_TESTS_MIGRATE = False
LANGUAGE_CODE = 'pt-BR'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
LANGUAGES =(
    ('pt-BR',u'Portugues'),
)
LOCALE_PATHS =(
    os.path.join(BASE_DIR,'/locale'),
)

USE_L10N = True
USE_TZ = True

STATIC_ROOT = '/var/www/tsmteste/'
STATIC_URL = '/static/'

STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
)
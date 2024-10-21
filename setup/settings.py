import os
from pathlib import Path
from django.contrib.messages import constants as messages

# ativa formatação de data para o admin
from django.conf.locale.pt_BR import formats as br_formats

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# formata a data do admin
br_formats.DATE_FORMAT = 'd/m/Y'

# formata a data do admin
br_formats.DATETIME_FORMAT = 'd/m/Y H:i:s'

# Para fazer com que as sessões permaneçam abertas somente enquanto o navegador estiver aberto
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Para que a sessão seja renovada a cada requisição (apenas em DEBUG)
#SESSION_SAVE_EVERY_REQUEST = True

# limitar o tempo da sessão em 14 min
#SESSION_COOKIE_AGE = 840

# salva a sessão do usuário
#SESSION_SAVE_EVERY_REQUEST = True

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-hs3ict6^9oac@bljhij^78j2mcyqwdhczoxgl2_3d*-2er64y9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'core', 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'setup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR / 'templates')],
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

WSGI_APPLICATION = 'setup.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Rio_Branco'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

#localização dos arquivos de static
STATIC_URL = 'static/'
STATIC_ROOT =os.path.join(BASE_DIR / 'static_collected')
STATICFILES_DIRS = [os.path.join(BASE_DIR / 'static')]

#localização dos arquivos de media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR / 'media')
LOGIN_URL = 'login_new'

#Definição de tamanho maximo de arquivo armazenado na memoria ram do servidor, NÃO UTILIZE
#FILE_UPLOAD_MAX_MEMORY_SIZE = 

# tags de mensagens
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'core.User'




from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET KEY ESPOSTA
SECRET_KEY = 'django-insecure-fk$+4-@mfjf1_j3a_0a-f=*2!%^sm3_ndjj)nzskv+4&@s4ks1'

# DEBUG ATTIVO
DEBUG = True

ALLOWED_HOSTS = []


# Insieme app

INSTALLED_APPS = [
    'daphne',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    'bootstrap_datepicker_plus',
    'utenti_custom',
    'gestione_utenti',
    'gestione_medici',
    'gestione_assistenza'
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

ROOT_URLCONF = 'sito_prenotazioni.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'sito_prenotazioni.wsgi.application'
ASGI_APPLICATION = 'sito_prenotazioni.asgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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

# Lingua e fuso orario cambiati per l'Italia
LANGUAGE_CODE = 'it'

TIME_ZONE = 'Europe/Rome'

USE_I18N = True

USE_TZ = True

# path file statici
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,"static")]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# modello utente custom
AUTH_USER_MODEL = 'utenti_custom.UtenteCustom'

# autenticazione default
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

# template usati da crispy forms
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# path file media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

LOGIN_REDIRECT_URL = '/?login=ok'
LOGOUT_REDIRECT_URL = '/utente/logout_riuscito'
LOGIN_URL = '/utente/login/?auth=notok'

# configurazioni per le email
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST_USER = "sito_prenotazioni@gmail.com"

# configurazioni per il pacchetto front-end per le date
BOOTSTRAP_DATEPICKER_PLUS = {
    "options": {
        "locale": "it",
    },
    "variant_options": {
        "datetime": {
            "format": "DD/MM/YYYY HH:mm",
        },
    }
}


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

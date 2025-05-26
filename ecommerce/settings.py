import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-votre-cle-secrete-ici'

DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop',  # Assurez-vous que 'shop' est bien ici
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



ROOT_URLCONF = 'ecommerce.urls'

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
                'shop.context_processors.site_config',  # Ajouter cette ligne
            ],
        },
    },
]


WSGI_APPLICATION = 'ecommerce.wsgi.application'

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

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

# Configuration des fichiers statiques
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Configuration des fichiers media
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'



# Créer les dossiers automatiquement
MEDIA_DIRS = [
    os.path.join(MEDIA_ROOT, 'categories'),
    os.path.join(MEDIA_ROOT, 'sous_categories'),
    os.path.join(MEDIA_ROOT, 'produits'),
    os.path.join(MEDIA_ROOT, 'site'),
    
]
# Créer les dossiers s'ils n'existent pas
for directory in MEDIA_DIRS:
    os.makedirs(directory, exist_ok=True)
    

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuration WhatsApp (IMPORTANT: Changez ce numéro)
WHATSAPP_NUMBER = "33123456789"  # Format international sans le +





# Hosts autorisés
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'sinlori-store-production.up.railway.app',  # Votre domaine Railway
    '.railway.app',  # Tous les sous-domaines Railway
]

# Origines de confiance pour CSRF
CSRF_TRUSTED_ORIGINS = [
    'https://sinlori-store-production.up.railway.app',
    'https://*.railway.app',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

# Configuration CSRF supplémentaire
CSRF_COOKIE_SECURE = not DEBUG  # True en production, False en développement
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'

# Session settings
SESSION_COOKIE_SECURE = not DEBUG  # True en production, False en développement
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'


if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
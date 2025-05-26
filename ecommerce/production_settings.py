from .settings import *
import os

DEBUG = False

ALLOWED_HOSTS = ['votre-domaine.com', 'www.votre-domaine.com']

# Base de données MySQL pour Hostinger
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'votre_db_name',
        'USER': 'votre_db_user',
        'PASSWORD': 'votre_db_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Configuration pour les fichiers statiques en production
STATIC_ROOT = '/path/to/static/files/'
MEDIA_ROOT = '/path/to/media/files/'

# Sécurité
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
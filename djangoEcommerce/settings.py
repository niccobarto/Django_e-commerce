import os
from pathlib import Path
from decouple import config
import dj_database_url
import django
import cloudinary
from django.contrib.auth import get_user_model

# Base directory del progetto
BASE_DIR = Path(__file__).resolve().parent.parent
ON_RENDER = os.environ.get('RENDER', False) == 'true'
# Sicurezza
SECRET_KEY = config('SECRET_KEY', default='unsafe-key')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='localhost,127.0.0.1' if not ON_RENDER else 'django-e-commerce-gbcg.onrender.com'
).split(',')
if ON_RENDER:
    CSRF_TRUSTED_ORIGINS = ['https://' + host for host in ALLOWED_HOSTS]

# App Django + app custom
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # App personalizzate
    "store",
    "accounts",
    "cart",
    "order",
    "management",

    # Plugin
    "django_countries",
    "widget_tweaks",
    "cloudinary_storage",
    "cloudinary",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Serve per servire i file statici in produzione
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "djangoEcommerce.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "djangoEcommerce.wsgi.application"

# Database (PostgreSQL su Render, fallback SQLite in locale)
DATABASE_URL = config('DATABASE_URL')

DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
}

# Modello utente personalizzato (se usato)
AUTH_USER_MODEL = 'accounts.CustomUser'

# Validatori password
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Localizzazione
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Rome"
USE_I18N = True
USE_TZ = True

# File statici (CSS, JS)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media su Cloudinary
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': config('CLOUDINARY_API_KEY'),
    'API_SECRET': config('CLOUDINARY_API_SECRET'),
}
cloudinary.config(
    cloud_name=config('CLOUDINARY_CLOUD_NAME'),
    api_key=config('CLOUDINARY_API_KEY'),
    api_secret=config('CLOUDINARY_API_SECRET')
)

# Media URL/ROOT (in caso di fallback locale)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Pagina di login
LOGIN_URL = '/accounts/login/'

# Chiave primaria default
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email backend disabilitato (solo per sviluppo/test: stampa in console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Superuser automatico su Render (opzionale)
if os.environ.get('RENDER_SUPERUSER', '') == 'true':
    django.setup()
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin'
        )

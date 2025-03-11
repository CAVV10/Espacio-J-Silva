# Carga las variables de entorno desde .env (para desarrollo local)
from dotenv import load_dotenv
load_dotenv()

import os
from pathlib import Path
from django.contrib.messages import constants as message_constants
import dj_database_url

# Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta (usa una diferente en producción)
SECRET_KEY = os.environ.get("SECRET_KEY", "clave-secreta-desarrollo")

# Modo debug (True para desarrollo, False para producción)
DEBUG = os.environ.get("DEBUG", "True") == "True"

# Hosts permitidos
ALLOWED_HOSTS = ['web-j-silva.onrender.com', 'localhost', '127.0.0.1']

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'cloudinary',                        # Cloudinary base
    'cloudinary_storage',               # Cloudinary storage para static/media
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.staticfiles',
    'contacto',                         # Tu app personalizada
]

# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Sirve archivos estáticos (útil si decides servir localmente)
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuración de URLs
ROOT_URLCONF = 'web_j_silva_ingenieria.urls'

# Configuración de plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Carpeta personalizada para templates
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

# WSGI
WSGI_APPLICATION = 'web_j_silva_ingenieria.wsgi.application'

# Base de datos: usa DATABASE_URL si está disponible (Render)
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
    }
else:
    # Configuración local (desarrollo)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get("DB_NAME", "mi_db"),
            'USER': os.environ.get("DB_USER", "admin"),
            'PASSWORD': os.environ.get("DB_PASSWORD", "1234"),
            'HOST': os.environ.get("DB_HOST", "localhost"),
            'PORT': os.environ.get("DB_PORT", "5432"),
        }
    }

# Validadores de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Configuración regional
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# === 📦 Cloudinary Configuration ===

# Archivos estáticos servidos desde Cloudinary
STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticCloudinaryStorage'

# Archivos de medios (subidos por usuarios) desde Cloudinary
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Configuración de Cloudinary (asegúrate de tener estas vars en Render o .env)
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}

# === Archivos estáticos y media (por si se usa localmente también) ===

STATIC_URL = '/static/'

# Directorios adicionales donde buscar archivos estáticos (útil en desarrollo)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'contacto', 'static', 'contacto'),
]

# Directorio donde Django recolecta los estáticos (cuando corres collectstatic)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Archivos de media (subidos por usuarios)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# === 📧 Configuración de correo ===
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = os.environ.get('EMAIL_ADMIN', '')

# === 👤 Autenticación personalizada ===
AUTH_USER_MODEL = 'contacto.CustomUser'
AUTHENTICATION_BACKENDS = [
    'contacto.backends.EmailBackend',  # Permite login con email
]

# === 🔐 Seguridad y sesión ===
LOGIN_URL = '/login/'  # Redirección si no está autenticado
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Seguridad (solo se activan si las vars están definidas como "True")
SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "False") == "True"
SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "False") == "True"
CSRF_COOKIE_SECURE = os.environ.get("CSRF_COOKIE_SECURE", "False") == "True"

# === ⚙️ Otras configuraciones ===
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Personalización de los mensajes flash
MESSAGE_TAGS = {
    message_constants.DEBUG: 'debug',
    message_constants.INFO: 'info',
    message_constants.SUCCESS: 'success',
    message_constants.WARNING: 'warning',
    message_constants.ERROR: 'error',
}

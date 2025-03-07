from django.contrib.messages import constants as message_constants
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Configuración rápida para el desarrollo; NO es adecuada para producción
# ADVERTENCIA: Mantén la clave secreta usada en producción en secreto.
SECRET_KEY = 'django-insecure-b*4%%5vjyf@948=bap_s9%kka9r^82lhr+x*1v9_6ax(8l0td^'

# ADVERTENCIA: No actives debug en producción
DEBUG = False

# Hosts permitidos en la aplicación
ALLOWED_HOSTS = ['*']

# Definición de aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.staticfiles',
    'contacto',  # Tu app personalizada
]

# Definición del middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Archivo principal de rutas
ROOT_URLCONF = 'web_j_silva_ingenieria.urls'

# Configuración de las plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# Configuración del WSGI
WSGI_APPLICATION = 'web_j_silva_ingenieria.wsgi.application'

# Configuración de la base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'j_silva_base_de_datos',  # Nombre de la base de datos
        'USER': 'jsilva_admin_base',      # Usuario de la base de datos
        'PASSWORD': 'adminjsilva',        # Contraseña del usuario
        'HOST': 'localhost',              # Host de la base de datos
        'PORT': '5432',                   # Puerto de la base de datos
    }
}

# Validación de contraseñas
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

# Internacionalización
LANGUAGE_CODE = 'es'

# Zona horaria para Colombia
USE_TZ = True
TIME_ZONE = 'America/Bogota'

# Archivos estáticos (CSS, JavaScript, Imágenes)
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'contacto', 'static', 'contacto'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Archivos de medios (para subir imágenes y otros archivos)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Configuración del correo electrónico
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'vargasvillanuevacarlosalberto@gmail.com'
EMAIL_HOST_PASSWORD = 'mmjy tlrh qouc iupj'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = 'vargasvillanuevacarlosalberto@gmail.com'

# Modelo de usuario personalizado
AUTH_USER_MODEL = 'contacto.CustomUser'

# Configuración de login y redirección
LOGIN_URL = '/login/'
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Configuraciones de seguridad para producción
SECURE_HSTS_SECONDS = 3600
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Tipo de campo de clave primaria por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MESSAGE_TAGS = {
    message_constants.DEBUG: 'debug',
    message_constants.INFO: 'info',
    message_constants.SUCCESS: 'success',
    message_constants.WARNING: 'warning',
    message_constants.ERROR: 'error',
}
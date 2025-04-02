import os
import sys

# Añade la ruta de tu proyecto al path de Python
# Ajusta esta ruta según la estructura de tu servidor en cPanel
path = '/home/senadsog/public_html'
if path not in sys.path:
    sys.path.insert(0, path)

# Configura las variables de entorno
os.environ['DJANGO_SETTINGS_MODULE'] = 'web_j_silva_ingenieria.settings'

# Carga las variables de entorno desde .env
from dotenv import load_dotenv
load_dotenv(os.path.join(path, '.env'))

# Importa la aplicación WSGI de Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Opcional: Configuración para Passenger
# Si tienes problemas, puedes descomentar estas líneas
# import passenger.wsgi
# application = passenger.wsgi.application
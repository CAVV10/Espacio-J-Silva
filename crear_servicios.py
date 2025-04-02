import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_j_silva_ingenieria.settings')
django.setup()

from contacto.models import Servicio

# Verificar si hay servicios en la base de datos
servicios_count = Servicio.objects.count()
print(f"Número de servicios en la base de datos: {servicios_count}")

# Crear servicios si no existen
servicios_a_crear = [
    {"servicio_nombre": "Desinfección", "descripcion": "Servicio de desinfección de espacios"},
    {"servicio_nombre": "Control Apícola", "descripcion": "Servicio de control de abejas"},
    {"servicio_nombre": "Jardinería", "descripcion": "Servicio de mantenimiento de jardines"},
    {"servicio_nombre": "Capacitación", "descripcion": "Servicios de capacitación"}
]   

servicios_creados = 0
for servicio_data in servicios_a_crear:
    if not Servicio.objects.filter(servicio_nombre=servicio_data["servicio_nombre"]).exists():
        Servicio.objects.create(
            servicio_nombre=servicio_data["servicio_nombre"],
            descripcion=servicio_data["descripcion"]
        )
        servicios_creados += 1
        print(f"Servicio creado: {servicio_data['servicio_nombre']}")

print(f"Total de servicios creados: {servicios_creados}")
print(f"Total de servicios en la base de datos: {Servicio.objects.count()}")

# Listar todos los servicios
print("\nListado de todos los servicios:")
for servicio in Servicio.objects.all():
    print(f"ID: {servicio.id}, Nombre: {servicio.servicio_nombre}")
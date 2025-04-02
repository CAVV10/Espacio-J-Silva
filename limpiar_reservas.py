import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_j_silva_ingenieria.settings')
django.setup()

# Ahora podemos importar nuestros modelos
from contacto.models import Reserva
from django.utils import timezone
from datetime import timedelta

def limpiar_reservas():
    print("Iniciando limpieza de reservas...")
    
    # Verificar cuántas reservas hay en la base de datos
    reservas_count = Reserva.objects.count()
    print(f"Número de reservas en la base de datos: {reservas_count}")
    
    # Opción 1: Eliminar todas las reservas
    Reserva.objects.all().delete()
    
    # Verificar que se hayan eliminado
    reservas_count_after = Reserva.objects.count()
    print(f"Número de reservas después de la limpieza: {reservas_count_after}")
    
    print("Limpieza de reservas completada.")

if __name__ == "__main__":
    limpiar_reservas()


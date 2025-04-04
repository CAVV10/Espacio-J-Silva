from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User  # Importa el modelo de usuario
from cloudinary.models import CloudinaryField
from django.conf import settings  # Para usar settings.AUTH_USER_MODEL


class Mensaje(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField()
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensaje de {self.nombre} {self.apellido} - {self.correo}"

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
# Modelo Servicio (asegúrate de que tenga esta estructura)
class Servicio(models.Model):
    servicio_nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.servicio_nombre


class Reserva(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Relación con el usuario
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField()
    creado_en = models.DateTimeField(auto_now_add=True)

    numero_celular = models.CharField(max_length=15)  # Para almacenar el número de celular
    direccion = models.CharField(max_length=255)  # Para almacenar la dirección
    ciudad = models.CharField(max_length=100)  # Para almacenar la ciudad

    # Eliminamos la restricción de unicidad en Meta
    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['servicio', 'fecha_hora'],
    #             name='unique_reserva_servicio_fecha'
    #         )
    #     ]

    def __str__(self):
        return f'Reserva de {self.usuario} para {self.servicio} el {self.fecha_hora}'

    # Validaciones personalizadas antes de guardar
    def clean(self):
        # Verificar que el usuario esté asignado
        if not self.usuario_id:
            return  # Salir si el usuario no está asignado

        # Verificar si el servicio está asociado correctamente
        if self.servicio_id is None:
            raise ValidationError("La reserva debe tener un servicio asignado.")
        
        # Validar fecha y hora
        if self.fecha_hora is None:
            raise ValidationError("La fecha y hora de la reserva no pueden estar vacías.")

        # Validación: Las reservas solo están disponibles entre las 7 a.m. y las 7 p.m.
        if not (7 <= self.fecha_hora.hour <= 19):
            raise ValidationError("Las reservas solo están disponibles entre las 7 a.m. y las 7 p.m.")

        # Validación: No se puede reservar con más de 30 días de anticipación
        fecha_maxima = timezone.now() + timedelta(days=30)
        if self.fecha_hora > fecha_maxima:
            raise ValidationError("No se pueden hacer reservas con más de 30 días de anticipación.")

        # Validación: No se puede hacer una reserva en una fecha pasada
        if self.fecha_hora < timezone.now():
            raise ValidationError("No puedes hacer una reserva en una fecha pasada.")

        # Eliminamos la validación de reservas duplicadas
        # reservas_existentes = Reserva.objects.filter(
        #     servicio=self.servicio, 
        #     fecha_hora=self.fecha_hora
        # )
        # 
        # if self.pk:
        #     reservas_existentes = reservas_existentes.exclude(pk=self.pk)
        #     
        # if reservas_existentes.exists():
        #     raise ValidationError("Ya existe una reserva para este servicio en la fecha y hora seleccionadas. Por favor, elige otra fecha u hora.")

    def save(self, *args, **kwargs):
        # Llama a clean() antes de guardar para asegurarse de que las validaciones se ejecuten
        self.full_clean()  # Cambiado de self.clean() a self.full_clean()
        super(Reserva, self).save(*args, **kwargs)

class HistorialCompra(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    # Otros campos relevantes para la compra

    def __str__(self):
        return f"Compra {self.id} de {self.usuario.username}"

class HistorialReserva(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField()
    servicio = models.CharField(max_length=100)
    # Otros campos relevantes para la reserva

    def __str__(self):
        return f"Reserva {self.id} de {self.usuario.username}"




class OpcionProducto(models.Model):
    producto = models.ForeignKey('Producto', related_name='opciones', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    valor = models.CharField(max_length=100)
    opciones = models.JSONField(default=list)  # Ej: [{"valor": "CO2", "precio": 75000}, {"valor": "ABC", "precio": 85000}]


    def __str__(self):
        return f"{self.producto.nombre} - {self.nombre}: {self.valor}"
    
    class Meta:
        verbose_name = "Opción de producto"
        verbose_name_plural = "Opciones de productos"

class Producto(models.Model):
    TIPO_CHOICES = [
        ('general', 'General'),
        ('extintor', 'Extintor'),
        ('plano_3d', 'Plano 3D'),
    ]

    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='general')
    descripcion = models.TextField()
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = CloudinaryField('image', blank=True, null=True)
    activo = models.BooleanField(default=True)
    tiene_opciones = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

from django.core.mail import EmailMessage
from django.utils import timezone
from datetime import timedelta
from django import forms
from django.conf import settings

import os

def enviar_correo_confirmacion(reserva):
    # Datos del usuario y empresa
    usuario = reserva.usuario
    servicio = reserva.servicio
    fecha_hora = reserva.fecha_hora.strftime('%d/%m/%Y %H:%M:%S')
    correo_usuario = usuario.email
    correo_empresa = settings.EMAIL_HOST_USER

    # Asunto y contenido del correo para el usuario
    asunto_usuario = "Confirmación de Reserva - J Silva Ingeniería"
    mensaje_usuario = f"""
    Hola {usuario.first_name},

    Su reserva para el servicio {servicio.servicio_nombre} ha sido confirmada.

    Fecha y hora: {fecha_hora}

    ¡Gracias por confiar en nosotros!

    Atentamente,
    El equipo de J Silva Ingeniería
    """

    # Asunto y contenido del correo para la empresa
    asunto_empresa = f"Nueva Reserva de {usuario.first_name} {usuario.last_name}"
    mensaje_empresa = f"""
    Ha recibido una nueva reserva:

    Cliente: {usuario.first_name} {usuario.last_name}
    Correo: {correo_usuario}
    Servicio: {servicio.servicio_nombre}
    Fecha y hora: {fecha_hora}

    Atentamente,
    El sistema de reservas
    """

    try:
        # Enviar correo al usuario
        email_usuario = EmailMessage(asunto_usuario, mensaje_usuario, settings.EMAIL_HOST_USER, [correo_usuario])
        email_usuario.send(fail_silently=False)

        # Enviar correo a la empresa
        email_empresa = EmailMessage(asunto_empresa, mensaje_empresa, settings.EMAIL_HOST_USER, [correo_empresa])
        email_empresa.send(fail_silently=False)

        print("Correos enviados con éxito.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")  # Loguear el error o manejarlo como prefieras
        raise  # Vuelve a lanzar la excepción si deseas manejarla en otro lugar

def validar_fecha_hora(fecha_hora):
    ahora = timezone.now()
    if fecha_hora < ahora:
        raise forms.ValidationError("La fecha y hora no pueden estar en el pasado.")
    elif fecha_hora > ahora + timedelta(days=90):
        raise forms.ValidationError("Solo puede reservarse hasta con 3 meses de anticipación.")
    return fecha_hora
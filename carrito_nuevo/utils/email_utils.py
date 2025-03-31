from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.urls import reverse
import datetime

def enviar_correo_confirmacion_pedido(pedido, items):
    """
    Envía un correo electrónico de confirmación al cliente con los detalles del pedido.
    
    Args:
        pedido: Objeto Pedido con la información del pedido
        items: Lista de items del pedido
    """
    # Contexto para el template
    context = {
        'pedido': pedido,
        'items': items,
        'site_url': settings.SITE_URL,
        'year': datetime.datetime.now().year
    }
    
    # Renderizar el template HTML
    html_content = render_to_string('carrito_nuevo/emails/confirmacion_pedido.html', context)
    
    # Crear versión de texto plano para clientes de correo que no soportan HTML
    text_content = strip_tags(html_content)
    
    # Crear el correo
    subject = f'Confirmación de Pedido #{pedido.id} - J Silva Ingeniería'
    from_email = settings.DEFAULT_FROM_EMAIL
    to = pedido.usuario.email
    
    # Crear el mensaje
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    
    # Enviar el correo
    return msg.send()

def enviar_notificacion_admin_pedido(pedido, items):
    """
    Envía un correo electrónico de notificación al administrador cuando se recibe un nuevo pedido.
    
    Args:
        pedido: Objeto Pedido con la información del pedido
        items: Lista de items del pedido
    """
    # Obtener el correo del administrador desde settings
    admin_email = getattr(settings, 'EMAIL_ADMIN', 'vargasvillanuevacarlosalberto@gmail.com')
    
    # Contexto para el template
    context = {
        'pedido': pedido,
        'items': items,
        'site_url': settings.SITE_URL,
        'year': datetime.datetime.now().year
    }
    
    # Renderizar el template HTML
    html_content = render_to_string('carrito_nuevo/emails/notificacion_admin_pedido.html', context)
    
    # Crear versión de texto plano para clientes de correo que no soportan HTML
    text_content = strip_tags(html_content)
    
    # Crear el correo
    subject = f'Nueva Venta - Pedido #{pedido.id} - J Silva Ingeniería'
    from_email = settings.DEFAULT_FROM_EMAIL
    
    # Crear el mensaje
    msg = EmailMultiAlternatives(subject, text_content, from_email, [admin_email])
    msg.attach_alternative(html_content, "text/html")
    
    # Enviar el correo
    return msg.send()
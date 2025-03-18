from django import template
from carrito_nuevo.models import Carrito

register = template.Library()

@register.filter
def carrito_cantidad(user):
    """
    Devuelve la cantidad total de items en el carrito del usuario.
    Esta función reemplaza la versión anterior del template tag
    para usar el nuevo modelo de carrito.
    """
    if user.is_authenticated:
        try:
            carrito = Carrito.objects.filter(usuario=user, completado=False).first()
            if carrito:
                return carrito.cantidad_items
            return 0
        except Exception:
            return 0
    return 0

@register.simple_tag
def obtener_cantidad_carrito(user):
    """
    Template tag que devuelve la cantidad total de items en el carrito del usuario.
    Se usa como {% obtener_cantidad_carrito user %}
    """
    if user.is_authenticated:
        try:
            carrito = Carrito.objects.filter(usuario=user, completado=False).first()
            if carrito:
                return carrito.cantidad_items
            return 0
        except Exception:
            return 0
    return 0

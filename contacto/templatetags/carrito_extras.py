
from django import template

from contacto.models import Carrito
register = template.Library()

@register.filter
def carrito_cantidad(user):
    if user.is_authenticated:
        try:
            carrito = Carrito.objects.get(usuario=user)
            return sum(item.cantidad for item in carrito.itemcarrito_set.all())
        except Carrito.DoesNotExist:
            return 0
    return 0
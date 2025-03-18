from .models import Carrito

def carrito_context(request):
    """
    Context processor para hacer disponible la cantidad de items en el carrito
    en todas las plantillas.
    """
    carrito_cantidad = 0
    if request.user.is_authenticated:
        try:
            carrito = Carrito.objects.get(usuario=request.user)
            carrito_cantidad = sum(item.cantidad for item in carrito.itemcarrito_set.all())
        except Carrito.DoesNotExist:
            pass
    
    return {'carrito_cantidad': carrito_cantidad}

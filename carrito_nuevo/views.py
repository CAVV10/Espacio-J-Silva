from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.views.decorators.http import require_POST
from decimal import Decimal
from django.template.loader import render_to_string
from django.urls import reverse
from .utils.email_utils import enviar_correo_confirmacion_pedido, enviar_notificacion_admin_pedido




from .models import Producto, Categoria, Carrito, ItemCarrito, Pedido, EstadoPedido, ItemPedido, MetodoPago

# Vistas para catálogo y productos
def catalogo(request):
    """Vista principal de catálogo de productos"""
    categorias = Categoria.objects.filter(activo=True)
    
    # Filtros
    categoria_id = request.GET.get('categoria')
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    orden = request.GET.get('orden', 'nombre')  # Por defecto ordenar por nombre
    
    # Aplicar filtros
    productos = Producto.objects.filter(disponible=True)
    
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    
    if precio_min:
        productos = productos.filter(precio__gte=precio_min)
    
    if precio_max:
        productos = productos.filter(precio__lte=precio_max)
    
    # Aplicar ordenamiento
    if orden == 'precio_asc':
        productos = productos.order_by('precio')
    elif orden == 'precio_desc':
        productos = productos.order_by('-precio')
    elif orden == 'nombre':
        productos = productos.order_by('nombre')
    elif orden == 'destacado':
        productos = productos.order_by('-destacado', 'nombre')
    
    # Información del carrito para mostrar en la UI
    cantidad_carrito = 0
    if request.user.is_authenticated:
        carrito, _ = Carrito.objects.get_or_create(usuario=request.user, completado=False)
        cantidad_carrito = carrito.cantidad_items
    
    context = {
        'categorias': categorias,
        'productos': productos,
        'categoria_seleccionada': categoria_id,
        'precio_min': precio_min,
        'precio_max': precio_max,
        'orden': orden,
        'cantidad_carrito': cantidad_carrito
    }
    
    return render(request, 'carrito_nuevo/catalogo.html', context)

def detalle_producto(request, producto_id):
    """Vista de detalle de un producto específico"""
    producto = get_object_or_404(Producto, id=producto_id, disponible=True)
    
    # Productos relacionados (misma categoría)
    relacionados = Producto.objects.filter(
        categoria=producto.categoria, 
        disponible=True
    ).exclude(id=producto.id)[:4]
    
    context = {
        'producto': producto,
        'relacionados': relacionados
    }
    
    return render(request, 'carrito_nuevo/detalle_producto.html', context)

# Vistas para el carrito de compras
@login_required
def ver_carrito(request):
    """Vista para ver el contenido del carrito"""
    # Obtener o crear el carrito del usuario
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user, completado=False)
    
    # Obtener los items del carrito con sus datos
    items = carrito.items.select_related('producto').all()
    
    context = {
        'carrito': carrito,
        'items': items
    }
    
    return render(request, 'carrito_nuevo/carrito.html', context)


@require_POST
def agregar_al_carrito(request):
    """Añadir un producto al carrito"""
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if not authenticated

    producto_id = request.POST.get('producto_id')
    cantidad = int(request.POST.get('cantidad', 1))
    
    if not producto_id:
        return JsonResponse({
            'success': False,
            'message': 'Error: no se proporcionó un ID de producto'
        })
    
    # Verificar que el producto existe y está disponible
    try:
        producto = Producto.objects.get(id=producto_id, disponible=True)
    except Producto.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'El producto no existe o no está disponible'
        })
    
    # Verificar stock
    if producto.stock < cantidad:
        return JsonResponse({
            'success': False,
            'message': f'Solo hay {producto.stock} unidades disponibles'
        })
    
    # Obtener o crear el carrito
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user, completado=False)
    
    # Añadir el producto al carrito
    item, created = ItemCarrito.objects.get_or_create(
        carrito=carrito,
        producto=producto,
        defaults={'cantidad': cantidad}
    )
    
    # Si el producto ya estaba en el carrito, actualizar cantidad
    if not created:
        nueva_cantidad = item.cantidad + cantidad
        # Verificar stock nuevamente
        if nueva_cantidad > producto.stock:
            return JsonResponse({
                'success': False,
                'message': f'Solo hay {producto.stock} unidades disponibles'
            })
        
        item.cantidad = nueva_cantidad
        item.save()
    
    # Actualizar carrito
    carrito.save()
    
    return JsonResponse({
        'success': True,
        'message': f'{producto.nombre} añadido al carrito',
        'cantidad_carrito': carrito.cantidad_items,
        'total_carrito': carrito.total
    })


@require_POST
def agregar_al_carrito_ajax(request):
    """Añadir un producto al carrito mediante AJAX"""
    if not request.user.is_authenticated:
        return JsonResponse({
            'success': False,
            'redirect_url': reverse('contacto:login_view')  # Use the correct namespace and name
        })

    producto_id = request.POST.get('producto_id')
    cantidad = int(request.POST.get('cantidad', 1))
    
    if not producto_id:
        return JsonResponse({
            'success': False,
            'message': 'Error: no se proporcionó un ID de producto'
        })
    
    # Verificar que el producto existe y está disponible
    try:
        producto = Producto.objects.get(id=producto_id, disponible=True)
    except Producto.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'El producto no existe o no está disponible'
        })
    
    # Verificar stock
    if producto.stock < cantidad:
        return JsonResponse({
            'success': False,
            'message': f'Solo hay {producto.stock} unidades disponibles'
        })
    
    # Obtener o crear el carrito
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user, completado=False)
    
    # Añadir el producto al carrito
    item, created = ItemCarrito.objects.get_or_create(
        carrito=carrito,
        producto=producto,
        defaults={'cantidad': cantidad}
    )
    
    # Si el producto ya estaba en el carrito, actualizar cantidad
    if not created:
        nueva_cantidad = item.cantidad + cantidad
        # Verificar stock nuevamente
        if nueva_cantidad > producto.stock:
            return JsonResponse({
                'success': False,
                'message': f'Solo hay {producto.stock} unidades disponibles'
            })
        
        item.cantidad = nueva_cantidad
        item.save()
    
    # Actualizar carrito
    carrito.save()
    
    return JsonResponse({
        'success': True,
        'message': f'{producto.nombre} añadido al carrito',
        'cantidad_total': carrito.cantidad_items,
        'total_carrito': float(carrito.total),
        'total_formateado': carrito.total_formateado
    })


def catalogo_productos(request):
    """Mostrar catálogo de productos"""
    productos = Producto.objects.filter(disponible=True)
    return render(request, 'catalogo_productos.html', {'productos': productos})

@login_required
@require_POST
def actualizar_cantidad(request):
    """Actualizar la cantidad de un producto en el carrito"""
    item_id = request.POST.get('item_id')
    cantidad = int(request.POST.get('cantidad', 1))
    
    if not item_id:
        return JsonResponse({
            'success': False,
            'message': 'Error: no se proporcionó un ID de item'
        })
    
    # Verificar que el item existe
    try:
        item = ItemCarrito.objects.select_related('producto', 'carrito').get(
            id=item_id, 
            carrito__usuario=request.user,
            carrito__completado=False
        )
    except ItemCarrito.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'El item no existe en su carrito'
        })
    
    # Verificar que la cantidad es válida
    if cantidad <= 0:
        return JsonResponse({
            'success': False,
            'message': 'La cantidad debe ser mayor a cero'
        })
    
    # Verificar stock
    if cantidad > item.producto.stock:
        return JsonResponse({
            'success': False,
            'message': f'Solo hay {item.producto.stock} unidades disponibles'
        })
    
    # Actualizar cantidad
    item.cantidad = cantidad
    item.save()
    
    # Recalcular totales
    carrito = item.carrito
    
    return JsonResponse({
        'success': True,
        'message': 'Cantidad actualizada',
        'subtotal': float(item.subtotal),
        'subtotal_formateado': item.subtotal_formateado,
        'total_carrito': float(carrito.total),
        'total_formateado': f"${carrito.total:,.0f}".replace(",", ".")
    })

@login_required
@require_POST
def actualizar_cantidad_ajax(request):
    """Actualizar la cantidad de un producto en el carrito mediante AJAX"""
    item_id = request.POST.get('item_id')
    cantidad = int(request.POST.get('cantidad', 1))
    
    if not item_id:
        return JsonResponse({
            'success': False,
            'message': 'Error: no se proporcionó un ID de item'
        })
    
    # Verificar que el item existe
    try:
        item = ItemCarrito.objects.select_related('producto', 'carrito').get(
            id=item_id, 
            carrito__usuario=request.user,
            carrito__completado=False
        )
    except ItemCarrito.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'El item no existe en su carrito'
        })
    
    # Verificar que la cantidad es válida
    if cantidad <= 0:
        return JsonResponse({
            'success': False,
            'message': 'La cantidad debe ser mayor a cero'
        })
    
    # Verificar stock
    if cantidad > item.producto.stock:
        return JsonResponse({
            'success': False,
            'message': f'Solo hay {item.producto.stock} unidades disponibles'
        })
    
    # Actualizar cantidad
    item.cantidad = cantidad
    item.save()
    
    # Recalcular totales
    carrito = item.carrito
    carrito.save()
    
    # Calcular la cantidad total de productos en el carrito
    cantidad_total = carrito.items.aggregate(total=Sum('cantidad'))['total'] or 0
    
    return JsonResponse({
        'success': True,
        'message': 'Cantidad actualizada',
        'cantidad': cantidad,
        'subtotal': float(item.subtotal),
        'subtotal_formateado': item.subtotal_formateado,
        'total': float(carrito.total),
        'total_formateado': carrito.total_formateado,
        'cantidad_total': cantidad_total
    })

@login_required
@require_POST
def eliminar_del_carrito(request):
    """Eliminar un producto del carrito"""
    item_id = request.POST.get('item_id')
    
    if not item_id:
        return JsonResponse({
            'success': False,
            'message': 'Error: no se proporcionó un ID de item'
        })
    
    # Verificar que el item existe
    try:
        item = ItemCarrito.objects.select_related('carrito').get(
            id=item_id, 
            carrito__usuario=request.user,
            carrito__completado=False
        )
    except ItemCarrito.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'El item no existe en su carrito'
        })
    
    # Guardar referencia al carrito antes de eliminar
    carrito = item.carrito
    
    # Eliminar el item
    nombre_producto = item.producto.nombre
    item.delete()
    
    # Recalcular total
    nuevo_total = carrito.total
    
    return JsonResponse({
        'success': True,
        'message': f'{nombre_producto} eliminado del carrito',
        'total_carrito': float(nuevo_total),
        'total_formateado': f"${nuevo_total:,.0f}".replace(",", "."),
        'carrito_vacio': carrito.esta_vacio
    })

@login_required
@require_POST
def eliminar_del_carrito_ajax(request):
    """Eliminar un producto del carrito mediante AJAX"""
    item_id = request.POST.get('item_id')
    
    if not item_id:
        return JsonResponse({
            'success': False,
            'message': 'Error: no se proporcionó un ID de item'
        })
    
    # Verificar que el item existe
    try:
        item = ItemCarrito.objects.select_related('carrito', 'producto').get(
            id=item_id, 
            carrito__usuario=request.user,
            carrito__completado=False
        )
    except ItemCarrito.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'El item no existe en su carrito'
        })
    
    # Guardar referencia al carrito antes de eliminar
    carrito = item.carrito
    
    # Eliminar el item
    nombre_producto = item.producto.nombre
    item.delete()
    
    # Recalcular total
    nuevo_total = carrito.total
    
    # Calcular la cantidad total de productos en el carrito
    cantidad_total = carrito.items.aggregate(total=Sum('cantidad'))['total'] or 0
    items_count = carrito.items.count()
    
    return JsonResponse({
        'success': True,
        'message': f'{nombre_producto} eliminado del carrito',
        'total_carrito': float(nuevo_total),
        'total_formateado': carrito.total_formateado,
        'carrito_vacio': carrito.esta_vacio,
        'cantidad_total': cantidad_total,
        'items_count': items_count
    })

@login_required
def vaciar_carrito(request):
    """Eliminar todos los productos del carrito"""
    if request.method == 'POST':
        # Obtener el carrito del usuario
        try:
            carrito = Carrito.objects.get(usuario=request.user, completado=False)
            # Eliminar todos los items
            carrito.items.all().delete()
            
            return JsonResponse({
                'success': True,
                'message': 'Carrito vaciado correctamente'
            })
        except Carrito.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'No se encontró un carrito activo'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Método no permitido'
    })

@login_required
@require_POST
def vaciar_carrito_ajax(request):
    """Eliminar todos los productos del carrito mediante AJAX"""
    # Obtener carrito del usuario
    try:
        carrito = Carrito.objects.get(usuario=request.user, completado=False)
    except Carrito.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'No tiene un carrito activo'
        })
    
    # Eliminar todos los items
    carrito.items.all().delete()
    
    # Recalcular totales
    carrito.save()
    
    return JsonResponse({
        'success': True,
        'message': 'Carrito vaciado correctamente',
        'total_carrito': float(carrito.total),
        'total_formateado': carrito.total_formateado,
        'cantidad_total': 0,
        'items_count': 0
    })

# Vistas para proceso de checkout
@login_required
def checkout(request):
    """Vista para el proceso de checkout"""
    # Obtener carrito del usuario
    try:
        carrito = Carrito.objects.get(usuario=request.user, completado=False)
        
        # Verificar que el carrito no esté vacío
        if carrito.esta_vacio:
            return redirect('carrito_nuevo:ver_carrito')
        
        items = carrito.items.select_related('producto').all()
        
        context = {
            'carrito': carrito,
            'items': items
        }
        
        return render(request, 'carrito_nuevo/checkout.html', context)
    
    except Carrito.DoesNotExist:
        return redirect('carrito_nuevo:catalogo')

@login_required
def comprobacion(request):
    """Vista para la comprobación final y proceso de pago"""
    # Obtener carrito del usuario
    try:
        carrito = Carrito.objects.get(usuario=request.user, completado=False)
        
        # Verificar que el carrito no esté vacío
        if carrito.esta_vacio:
            return redirect('carrito_nuevo:ver_carrito')
        
        items = carrito.items.select_related('producto').all()
        
        # Obtener métodos de pago activos ordenados
        metodos_pago = MetodoPago.objects.filter(activo=True).order_by('orden', 'nombre')
        metodo_predeterminado = MetodoPago.objects.filter(es_predeterminado=True, activo=True).first()
        
        context = {
            'carrito': carrito,
            'items': items,
            'metodos_pago': metodos_pago,
            'metodo_predeterminado': metodo_predeterminado
        }
        
        return render(request, 'carrito_nuevo/comprobacion.html', context)
    
    except Carrito.DoesNotExist:
        return redirect('carrito_nuevo:catalogo')

@login_required
@require_POST
def procesar_pedido(request):
    """Procesar un nuevo pedido"""
    try:
        carrito = Carrito.objects.get(usuario=request.user, completado=False)
        
        # Verificar que el carrito no esté vacío
        if carrito.esta_vacio:
            return JsonResponse({'error': 'El carrito está vacío'}, status=400)
        
        # Obtener datos del formulario
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        direccion = request.POST.get('direccion')
        ciudad = request.POST.get('ciudad')
        telefono = request.POST.get('telefono')
        metodo_pago_id = request.POST.get('metodo_pago')
        
        # Validar datos mínimos
        if not all([nombre, email, direccion, ciudad, telefono, metodo_pago_id]):
            return JsonResponse({'error': 'Todos los campos son requeridos'}, status=400)
            
        # Obtener el método de pago
        try:
            metodo_pago = MetodoPago.objects.get(id=metodo_pago_id, activo=True)
        except MetodoPago.DoesNotExist:
            return JsonResponse({'error': 'El método de pago seleccionado no es válido'}, status=400)
        
        # Generar la dirección completa
        direccion_completa = f"{direccion}, {ciudad}"
        
        # Crear el pedido
        estado_pendiente = EstadoPedido.objects.get(nombre='Pendiente')
        pedido = Pedido.objects.create(
            usuario=request.user,
            estado=estado_pendiente,
            direccion_entrega=direccion_completa,
            telefono_contacto=telefono,
            total=carrito.total,
            metodo_pago=metodo_pago,
            notas=f"Pedido realizado por {nombre} ({email})"
        )
        
        # Transferir items del carrito al pedido y actualizar stock
        for item in carrito.items.all():
            # Crear el ítem de pedido
            ItemPedido.objects.create(
                pedido=pedido,
                producto=item.producto,
                cantidad=item.cantidad,
                precio_unitario=item.precio_unitario,
                subtotal=item.subtotal
            )
            
            # Actualizar el stock del producto
            producto = item.producto
            if producto.stock >= item.cantidad:
                producto.stock -= item.cantidad
                producto.save()
            else:
                # Si no hay suficiente stock, ajustar al máximo disponible
                producto.stock = 0
                producto.save()
        
        # Marcar el carrito como completado
        carrito.completado = True
        carrito.save()
        
        # Obtener los items del pedido para los correos
        items = pedido.items.select_related('producto').all()
        
        # Enviar correo de confirmación al cliente
        enviar_correo_confirmacion_pedido(pedido, items)
        
        # Enviar notificación al administrador
        enviar_notificacion_admin_pedido(pedido, items)
        
        # Redirigir a la página de confirmación
        url_confirmacion = reverse('carrito_nuevo:confirmacion_pedido', args=[pedido.id])
        
        return JsonResponse({'success': True, 'redirect_url': url_confirmacion})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def confirmacion_pedido(request, pedido_id):
    """Vista de confirmación del pedido"""
    # Obtener el pedido y verificar que pertenezca al usuario
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    items = pedido.items.select_related('producto').all()
    
    context = {
        'pedido': pedido,
        'items': items
    }
    
    return render(request, 'carrito_nuevo/confirmacion.html', context)

@login_required
def mis_pedidos(request):
    """Vista para ver los pedidos del usuario"""
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    
    context = {
        'pedidos': pedidos
    }
    
    return render(request, 'carrito_nuevo/mis_pedidos.html', context)

@login_required
def detalle_pedido(request, pedido_id):
    """Vista para ver el detalle de un pedido"""
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    items = pedido.items.select_related('producto').all()
    
    context = {
        'pedido': pedido,
        'items': items
    }
    
    return render(request, 'carrito_nuevo/detalle_pedido.html', context)

def filtrar_productos_ajax(request):
    if request.method == 'POST':
        # Obtener parámetros de filtro
        categoria_id = request.POST.get('categoria', '')
        precio_min = request.POST.get('precio_min', '')
        precio_max = request.POST.get('precio_max', '')
        
        # Iniciar con todos los productos
        productos = Producto.objects.all()
        
        # Filtrar por categoría si se especifica
        if categoria_id:
            productos = productos.filter(categoria_id=categoria_id)
        
        # Filtrar por precio mínimo si se especifica
        if precio_min:
            productos = productos.filter(precio__gte=float(precio_min))
        
        # Filtrar por precio máximo si se especifica
        if precio_max:
            productos = productos.filter(precio__lte=float(precio_max))
        
        # Obtener categorías para el contexto
        categorias = Categoria.objects.all()
        
        # Renderizar el HTML parcial con los productos filtrados
        html = render_to_string('carrito_nuevo/partials/productos_lista.html', {
            'productos': productos,
            'categoria_seleccionada': categoria_id,
            'precio_min': precio_min,
            'precio_max': precio_max,
            'categorias': categorias,
        }, request=request)
        
        # Devolver respuesta JSON con el HTML generado
        return JsonResponse({
            'success': True,
            'html': html,
            'count': productos.count()
        })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

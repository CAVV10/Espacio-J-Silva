from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'carrito_nuevo'

urlpatterns = [
    # Redirección de la URL base
    path('', RedirectView.as_view(pattern_name='carrito_nuevo:catalogo'), name='index'),
    
    # Catálogo y productos
    path('catalogo/', views.catalogo, name='catalogo'),
    path('catalogo/filtrar-ajax/', views.filtrar_productos_ajax, name='filtrar_productos_ajax'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    
    # Carrito
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/agregar-ajax/', views.agregar_al_carrito_ajax, name='agregar_al_carrito_ajax'),
    path('carrito/actualizar/', views.actualizar_cantidad, name='actualizar_cantidad'),
    path('carrito/actualizar-ajax/', views.actualizar_cantidad_ajax, name='actualizar_cantidad_ajax'),
    path('carrito/eliminar/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/eliminar-ajax/', views.eliminar_del_carrito_ajax, name='eliminar_del_carrito_ajax'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('carrito/vaciar-ajax/', views.vaciar_carrito_ajax, name='vaciar_carrito_ajax'),
    
    # Checkout y pedidos
    path('checkout/', views.checkout, name='checkout'),
    path('comprobacion/', views.comprobacion, name='comprobacion'),  # Nueva URL para la página de comprobación
    path('procesar-pedido/', views.procesar_pedido, name='procesar_pedido'),
    path('confirmacion/<int:pedido_id>/', views.confirmacion_pedido, name='confirmacion_pedido'),
    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),
    path('pedido/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
]

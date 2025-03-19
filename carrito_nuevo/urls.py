from django.urls import path
from . import views

app_name = 'carrito_nuevo'

urlpatterns = [
    # Catálogo y productos
    path('', views.catalogo, name='catalogo'),
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
    path('procesar-pedido/', views.procesar_pedido, name='procesar_pedido'),
    path('confirmacion/<int:pedido_id>/', views.confirmacion_pedido, name='confirmacion_pedido'),
    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),
    path('pedido/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
]

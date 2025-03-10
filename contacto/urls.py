# contacto/urls.py
from django.urls import path
from . import views
from .views import login_view, logout_view, obtener_reservas
from .views import password_reset_request, password_reset_confirm


urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('register/', views.register_view, name='register_view'),
    path('capacitacion/', views.capacitacion, name='capacitacion'),
    path('control-apicola/', views.control_apicola, name='control_apicola'),
    path('desinfeccion/', views.desinfeccion, name='desinfeccion'),
    path('jardineria/', views.jardineria, name='jardineria'),
    path('planos-3d/', views.planos_3d, name='planos_3d'),
    path('suministros/', views.suministros, name='suministros'),
    path('quienes-somos/', views.quienes_somos, name='quienes_somos'),
    path('hacer-reserva/', views.hacer_reserva, name='hacer_reserva'),
    path('obtener-eventos/', views.obtener_eventos, name='obtener_eventos'),
    path('enviar-mensaje/', views.enviar_mensaje, name='enviar_mensaje'),
    path('login/', login_view, name='login_view'),
    path('password-reset/', password_reset_request, name='password_reset_request'),
    path('password-reset-confirm/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
    path('agregar-al-carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', views.ver_carrito, name='carrito'),  # Añade esta línea
    path('carrito/eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/actualizar/<int:item_id>/', views.actualizar_cantidad, name='actualizar_cantidad'),
    path('carrito/pagar/', views.pagar, name='pagar'),
    path('panel-usuario/', views.panel_usuario_view, name='panel_usuario'),  # El nombre de la ruta es independiente del nombre del archivo
    path('obtener-reservas/', obtener_reservas, name='obtener_reservas'),
    path('ver-error-login/', views.ver_error_login),

    path('logout/', logout_view, name='logout'),
]

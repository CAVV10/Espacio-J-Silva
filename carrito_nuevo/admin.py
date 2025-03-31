from django.contrib import admin
from .models import Categoria, Producto, Carrito, ItemCarrito, EstadoPedido, Pedido, ItemPedido, MetodoPago

# Configuración de inlines
class ItemCarritoInline(admin.TabularInline):
    model = ItemCarrito
    extra = 0

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ['producto', 'cantidad', 'precio_unitario', 'subtotal']

# Registros en el admin
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo', 'fecha_creacion']
    list_filter = ['activo']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['activo']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'stock', 'disponible', 'destacado']
    list_filter = ['categoria', 'disponible', 'destacado']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['precio', 'stock', 'disponible', 'destacado']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    fieldsets = [
        ('Información básica', {'fields': ['nombre', 'descripcion', 'categoria']}),
        ('Imagen', {'fields': ['imagen']}),
        ('Precios y disponibilidad', {'fields': ['precio', 'stock', 'disponible', 'destacado']}),
        ('Fechas', {'fields': ['fecha_creacion', 'fecha_actualizacion'], 'classes': ['collapse']}),
    ]

@admin.register(MetodoPago)
class MetodoPagoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'activo', 'es_predeterminado', 'requiere_tarjeta', 'orden']
    list_filter = ['activo', 'es_predeterminado', 'requiere_tarjeta']
    search_fields = ['nombre', 'codigo', 'descripcion']
    list_editable = ['activo', 'es_predeterminado', 'requiere_tarjeta', 'orden']
    prepopulated_fields = {'codigo': ('nombre',)}
    fieldsets = [
        ('Información básica', {'fields': ['nombre', 'codigo', 'descripcion']}),
        ('Imagen', {'fields': ['imagen', 'imagen_path']}),
        ('Configuración', {'fields': ['activo', 'es_predeterminado', 'requiere_tarjeta', 'orden']}),
        ('Personalización de Confirmación', {
            'fields': [
                'instrucciones_confirmacion', 
                'codigo_qr', 
                'telefono_contacto', 
                'informacion_adicional'
            ],
            'classes': ['collapse'],
            'description': 'Configura cómo se mostrará este método de pago en la página de confirmación'
        }),
        ('Contenido HTML Personalizado', {
            'fields': ['contenido_html'],
            'classes': ['collapse'],
            'description': 'HTML personalizado para la página de confirmación. Puedes usar {{ pedido.total_formateado }}, {{ pedido.id }}, etc.'
        }),
    ]

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'creado', 'actualizado', 'completado', 'cantidad_items', 'total']
    list_filter = ['completado', 'creado']
    search_fields = ['usuario__username', 'usuario__email']
    readonly_fields = ['creado', 'actualizado']
    inlines = [ItemCarritoInline]

@admin.register(EstadoPedido)
class EstadoPedidoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre', 'descripcion']

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'fecha_creacion', 'estado', 'metodo_pago', 'total']
    list_filter = ['estado', 'metodo_pago', 'fecha_creacion']
    search_fields = ['usuario__username', 'usuario__email', 'direccion_entrega']
    readonly_fields = ['fecha_creacion', 'total']
    inlines = [ItemPedidoInline]

@admin.register(ItemCarrito)
class ItemCarritoAdmin(admin.ModelAdmin):
    list_display = ['carrito', 'producto', 'cantidad', 'precio_unitario', 'subtotal']
    list_filter = ['carrito', 'producto']
    search_fields = ['carrito__usuario__username', 'carrito__usuario__email', 'producto__nombre']

@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'producto', 'cantidad', 'precio_unitario', 'subtotal']
    list_filter = ['pedido', 'producto']
    search_fields = ['pedido__usuario__username', 'pedido__usuario__email', 'producto__nombre']

# Comenta o elimina esta sección:
# @admin.register(CarritoItem)
# class CarritoItemAdmin(admin.ModelAdmin):
#     list_display = ['carrito', 'producto', 'cantidad', 'precio_unitario', 'subtotal']
#     list_filter = ['carrito', 'producto']
#     search_fields = ['carrito__usuario__username', 'carrito__usuario__email', 'producto__nombre']

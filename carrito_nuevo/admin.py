from django.contrib import admin
from .models import Categoria, Producto, Carrito, ItemCarrito, EstadoPedido, Pedido, ItemPedido

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
    list_display = ['id', 'usuario', 'fecha_creacion', 'estado', 'total']
    list_filter = ['estado', 'fecha_creacion']
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

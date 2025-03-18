from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Mensaje, 
    CustomUser, 
    Servicio, 
    Reserva, 
    Producto, 
    OpcionProducto
)

class OpcionProductoInline(admin.TabularInline):
    model = OpcionProducto
    extra = 1
    fields = ('nombre', 'opciones')
    verbose_name = "Opción"
    verbose_name_plural = "Opciones"

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'precio_base', 'activo')
    list_filter = ('tipo', 'activo')
    search_fields = ('nombre', 'descripcion')
    inlines = [OpcionProductoInline]
    
    fieldsets = (
        ('Información básica', {
            'fields': ('nombre', 'tipo', 'descripcion', 'imagen')
        }),
        ('Precios y estado', {
            'fields': ('precio_base', 'activo')
        }),
    )

# Registrar los demás modelos
admin.site.register(Mensaje)
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Servicio)
admin.site.register(Reserva)
from django.db import models
from django.conf import settings
from decimal import Decimal

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    disponible = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nombre
    
    @property
    def precio_formateado(self):
        return f"${self.precio:,.0f}".replace(",", ".")
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-destacado', 'nombre']

class Carrito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carrito_nuevo_set')
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    completado = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Carrito de {self.usuario.username}"
    
    @property
    def total(self):
        items = self.items.all()
        return sum(item.subtotal for item in items)
    
    @property
    def cantidad_items(self):
        items = self.items.all()
        return sum(item.cantidad for item in items)
    
    @property
    def esta_vacio(self):
        return self.items.count() == 0
    
    class Meta:
        verbose_name = "Carrito"
        verbose_name_plural = "Carritos"

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
    
    @property
    def subtotal(self):
        return self.producto.precio * Decimal(self.cantidad)
    
    @property
    def precio_unitario(self):
        return self.producto.precio
    
    @property
    def subtotal_formateado(self):
        return f"${self.subtotal:,.0f}".replace(",", ".")
    
    class Meta:
        verbose_name = "Item de Carrito"
        verbose_name_plural = "Items de Carrito"
        unique_together = ('carrito', 'producto')

class EstadoPedido(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Estado de Pedido"
        verbose_name_plural = "Estados de Pedido"

class Pedido(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pedido_nuevo_set')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.ForeignKey(EstadoPedido, on_delete=models.PROTECT)
    direccion_entrega = models.TextField(blank=True, null=True)
    telefono_contacto = models.CharField(max_length=20, blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username}"
    
    @property
    def total_formateado(self):
        return f"${self.total:,.0f}".replace(",", ".")
    
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-fecha_creacion']

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
    
    @property
    def subtotal_formateado(self):
        return f"${self.subtotal:,.0f}".replace(",", ".")
    
    class Meta:
        verbose_name = "Item de Pedido"
        verbose_name_plural = "Items de Pedido"

from django.core.management.base import BaseCommand
from carrito_nuevo.models import Categoria, Producto
from decimal import Decimal

class Command(BaseCommand):
    help = 'Crea productos de prueba para la nueva aplicación de carrito'

    def handle(self, *args, **kwargs):
        # Crear categorías
        categorias = {
            'Herramientas': 'Herramientas profesionales para construcción',
            'Materiales': 'Materiales de alta calidad para obras',
            'Equipos': 'Equipos especializados para ingeniería',
            'Seguridad': 'Elementos de protección y seguridad',
        }
        
        categoria_objs = {}
        for nombre, descripcion in categorias.items():
            cat, created = Categoria.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'descripcion': descripcion,
                    'activo': True
                }
            )
            categoria_objs[nombre] = cat
            if created:
                self.stdout.write(self.style.SUCCESS(f'Categoría creada: {nombre}'))
            else:
                self.stdout.write(self.style.WARNING(f'Categoría ya existente: {nombre}'))
        
        # Crear productos
        productos = [
            {
                'nombre': 'Martillo Profesional',
                'descripcion': 'Martillo de alta resistencia con mango ergonómico',
                'precio': Decimal('45.99'),
                'stock': 50,
                'destacado': True,
                'categoria': categoria_objs['Herramientas'],
                'imagen': 'productos/martillo.jpg'
            },
            {
                'nombre': 'Cemento Premium',
                'descripcion': 'Saco de cemento de 50kg de alta calidad',
                'precio': Decimal('15.50'),
                'stock': 100,
                'destacado': True,
                'categoria': categoria_objs['Materiales'],
                'imagen': 'productos/cemento.jpg'
            },
            {
                'nombre': 'Nivel Láser',
                'descripcion': 'Nivel láser profesional con trípode incluido',
                'precio': Decimal('129.99'),
                'stock': 15,
                'destacado': True,
                'categoria': categoria_objs['Equipos'],
                'imagen': 'productos/nivel.jpg'
            },
            {
                'nombre': 'Casco de Seguridad',
                'descripcion': 'Casco de seguridad certificado para construcción',
                'precio': Decimal('25.00'),
                'stock': 75,
                'destacado': False,
                'categoria': categoria_objs['Seguridad'],
                'imagen': 'productos/casco.jpg'
            },
            {
                'nombre': 'Taladro Inalámbrico',
                'descripcion': 'Taladro inalámbrico 20V con batería de larga duración',
                'precio': Decimal('189.99'),
                'stock': 20,
                'destacado': True,
                'categoria': categoria_objs['Herramientas'],
                'imagen': 'productos/taladro.jpg'
            },
            {
                'nombre': 'Ladrillos Refractarios',
                'descripcion': 'Paquete de 10 ladrillos refractarios para alta temperatura',
                'precio': Decimal('49.50'),
                'stock': 60,
                'destacado': False,
                'categoria': categoria_objs['Materiales'],
                'imagen': 'productos/ladrillos.jpg'
            },
            {
                'nombre': 'Medidor de Distancia',
                'descripcion': 'Medidor de distancia láser digital con precisión milimétrica',
                'precio': Decimal('79.99'),
                'stock': 25,
                'destacado': False,
                'categoria': categoria_objs['Equipos'],
                'imagen': 'productos/medidor.jpg'
            },
            {
                'nombre': 'Guantes de Trabajo',
                'descripcion': 'Par de guantes de trabajo resistentes a cortes',
                'precio': Decimal('12.99'),
                'stock': 100,
                'destacado': False,
                'categoria': categoria_objs['Seguridad'],
                'imagen': 'productos/guantes.jpg'
            },
        ]
        
        for producto_data in productos:
            prod, created = Producto.objects.get_or_create(
                nombre=producto_data['nombre'],
                defaults=producto_data
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Producto creado: {producto_data["nombre"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'Producto ya existente: {producto_data["nombre"]}'))
                
        self.stdout.write(self.style.SUCCESS('Productos de prueba creados exitosamente'))

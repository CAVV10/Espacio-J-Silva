from django import template

register = template.Library()

@register.filter
def formato_producto_nombre(item):
    """
    Formatea el nombre del producto con sus opciones
    Uso en template: {{ item|formato_producto_nombre }}
    """
    nombre = item.producto.nombre
    if item.opciones:
        opciones = [valores['valor'] for valores in item.opciones.values()]
        return f"{nombre}, {', '.join(opciones)}"
    return nombre

@register.filter
def split(value, arg):
    """
    Divide una cadena usando el separador especificado
    Uso en template: {{ valor|split:',' }}
    """
    return value.split(arg)

@register.filter
def strip(value):
    """
    Elimina espacios en blanco al inicio y final
    Uso en template: {{ valor|strip }}
    """
    return value.strip()


@register.filter
def multiply(value, arg):
    """Multiplica dos números."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
    


@register.filter
def replace(value, arg):
    """
    Reemplaza caracteres en una cadena.
    Uso: {{ value|replace:"old,new" }}
    """
    old, new = arg.split(',')
    return value.replace(old, new)
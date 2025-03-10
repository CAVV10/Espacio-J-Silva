# Importaciones de Django
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import IntegrityError, transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import logging
logger = logging.getLogger(__name__)

import traceback



# Importaciones de terceros
import pytz

# Importaciones locales
from .forms import (
    MensajeForm, 
    ReservaForm, 
    PasswordResetForm, 
    PasswordResetConfirmForm,
    ExtintorForm,
    Plano3DForm
)
from .models import (
    CustomUser as User,
    Reserva,
    Servicio,
    Mensaje,
    Producto,
    Carrito,
    ItemCarrito,
    Pedido,
    ItemPedido
)
from .utils import enviar_correo_confirmacion, validar_fecha_hora

# Obtener el modelo de usuario personalizado
User = get_user_model()



# Vistas de las páginas principales
def inicio(request):
    return render(request, 'contacto/index.html')

def capacitacion(request):
    return render(request, 'contacto/capacitacion.html')

def control_apicola(request):
    return render(request, 'contacto/control-apicola.html')

def desinfeccion(request):
    return render(request, 'contacto/desinfeccion.html')

def jardineria(request):
    return render(request, 'contacto/jardineria.html')

def planos_3d(request):
    return render(request, 'contacto/planos-3d.html')

def suministros(request):
    return render(request, 'contacto/suministros.html')

def quienes_somos(request):
    return render(request, 'contacto/quienes-somos.html')

def panel_usuario_view(request):
    return render(request, 'contacto/panel-usuario.html')

# Función iniciar sesión
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').lower()
        password = request.POST.get('password', '')

        print(f"Intentando iniciar sesión con email: {email} y contraseña: {password}")

        try:
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({
                    'success': True,
                    'message': 'Inicio de sesión exitoso.',
                    'redirect_url': reverse('inicio')
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Correo o contraseña incorrectos.'
                })
        except Exception as e:
            import traceback
            error_msg = traceback.format_exc()
            print("🚨 Error en login_view:")
            print(error_msg)
            with open("/tmp/error_login.txt", "w") as f:
                    f.write(error_msg)

            return JsonResponse({'success': False, 'message': 'Error interno del servidor.'})



    return render(request, 'contacto/login.html')




def ver_error_login(request):
    if os.path.exists("/tmp/error_login.txt"):
        with open("/tmp/error_login.txt", "r") as f:
            contenido = f.read()
        return HttpResponse(f"<pre>{contenido}</pre>")
    else:
        return HttpResponse("No hay errores guardados.")




# Función cerrar sesión
def logout_view(request):
    logout(request)
    return redirect('inicio')

# Función registrarse
def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '').lower()  # Convertir a minúsculas
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if len(password1) < 6:
            return JsonResponse({'success': False, 'message': 'La contraseña debe tener al menos 6 caracteres.'})

        if password1 != password2:
            return JsonResponse({'success': False, 'message': 'Las contraseñas no coinciden.'})

        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'message': 'El correo ya está registrado.'})

        try:
            # Registrar usuario
            user = User.objects.create_user(
                email=email,  # Asegúrate de que el nombre de usuario sea el correo
                password=password1,
                first_name=first_name,
                last_name=last_name,
            )
            user.save()

            return JsonResponse({
                'success': True,
                'message': 'Registro exitoso. Ahora puede iniciar sesión.',
                'redirect_url': reverse('login_view')  # URL para redirigir después del registro
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Ocurrió un error inesperado: {}'.format(str(e))})

    # Si no es POST, devolvemos el mensaje de método no permitido
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})


# Función para recuperar contraseña
def password_reset_request(request):
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        email = request.POST.get('email')
        User = get_user_model()
        
        try:
            user = User.objects.get(email=email)
            # Generar token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Construir el enlace de restablecimiento
            reset_url = request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )
            
            # El mensaje directamente en la vista
            mensaje = f"""
            Hola {user.first_name},

            Ha solicitado restablecer su contraseña. Por favor, haga clic en el siguiente enlace para crear una nueva contraseña:

            {reset_url}

            Si no ha solicitado este cambio, puede ignorar este correo.

            Saludos,
            El equipo de J Silva Ingeniería
            """
            
            send_mail(
                'Solicitud de restablecimiento de contraseña',
                mensaje,
                settings.EMAIL_HOST_USER,  # Usar el email configurado en settings
                [user.email],
                fail_silently=False,
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Se ha enviado un enlace de restablecimiento a su correo electrónico.'
            })
            
        except User.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'No existe una cuenta asociada a este correo electrónico.'
            })
            
        except Exception as e:
            print(f"Error: {str(e)}")  # Para debugging
            return JsonResponse({
                'success': False,
                'message': 'Ocurrió un error al procesar su solicitud.'
            })
    
    return render(request, 'contacto/password_reset.html')

# Función para confirmar recuperación de contraseña
def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        validlink = default_token_generator.check_token(user, token)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        validlink = False

    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if user is not None and validlink:
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')
            
            if new_password1 and new_password2 and new_password1 == new_password2:
                try:
                    user.set_password(new_password1)
                    user.save()
                    return JsonResponse({
                        'success': True,
                        'message': 'Su contraseña ha sido actualizada correctamente.'
                    })
                except ValidationError as e:
                    return JsonResponse({
                        'success': False,
                        'message': str(e)
                    })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Las contraseñas no coinciden.'
                })
    
    return render(request, 'contacto/password_reset.html', {
        'validlink': validlink
    })


# Función para hacer reservas
@login_required
def hacer_reserva(request):
    servicios = Servicio.objects.all()
    productos = Producto.objects.all().prefetch_related('opciones')  # Añadir esta línea

    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario = request.user

            # Convertir la fecha y hora a la zona horaria de Bogotá
            bogota_tz = pytz.timezone('America/Bogota')
            fecha_hora_seleccionada = reserva.fecha_hora.astimezone(bogota_tz)

            # Validar que la fecha y hora no sean pasadas
            if fecha_hora_seleccionada < timezone.now().astimezone(bogota_tz):
                return JsonResponse({'success': False, 'message': 'No puede hacer una reserva en una fecha pasada.'})

            try:
                # Usar una transacción atómica para evitar condiciones de carrera
                with transaction.atomic():
                    # Guardar la reserva
                    reserva.save()  # Esto llamará a clean() y validará la reserva

                    # Si se guarda correctamente, enviar el correo de confirmación
                    enviar_correo_confirmacion(reserva)
                    return JsonResponse({'success': True, 'message': 'Reserva realizada con éxito.'})
            except IntegrityError:
                return JsonResponse({'success': False, 'message': 'Error: Ya existe una reserva para este servicio en la misma fecha y hora.'})
            except ValidationError as e:
                return JsonResponse({'success': False, 'message': str(e)})
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})
        else:
            errors = {field: error[0] for field, error in form.errors.items()}
            return JsonResponse({'success': False, 'message': 'El formulario no es válido.', 'errors': errors})
    else:
        form = ReservaForm()

 # Reemplazar el return existente con este:
    context = {
        'form': form,
        'servicios': servicios,
        'productos': productos,  # Agregamos los productos al contexto
    }
    return render(request, 'contacto/hacer-reserva.html', context)
# Función obtener reservas
def obtener_reservas(request):
    # Obtener todas las reservas futuras
    reservas = Reserva.objects.filter(fecha_hora__gte=timezone.now()).values_list('fecha_hora', flat=True)
    
    # Convertir las fechas y horas a un formato compatible con el frontend
    reservas_formateadas = [reserva.isoformat() for reserva in reservas]
    
    # Devolver las reservas en formato JSON
    return JsonResponse({'reservas': reservas_formateadas})


# Función para obtener eventos
def obtener_eventos(request):
    reservas = Reserva.objects.all()
    eventos = [{'title': f'Reserva de {reserva.usuario.email}', 'start': reserva.fecha_hora.isoformat()} for reserva in reservas]
    return JsonResponse(eventos, safe=False)





# Funciones para el carrito de compras
@login_required
def tienda_view(request):
    """Vista principal de la tienda"""
    productos = Producto.objects.filter(activo=True).prefetch_related('opciones')
    return render(request, 'contacto/tienda.html', {'productos': productos})

@login_required
def agregar_al_carrito(request, producto_id):
    if request.method == 'POST':
        try:
            producto = get_object_or_404(Producto, id=producto_id, activo=True)
            carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
            
            # Obtener datos del formulario
            cantidad = int(request.POST.get('cantidad', 1))
            opciones = {}
            precio_total = producto.precio_base

            # Recoger todas las opciones seleccionadas y sus precios
            for opcion in producto.opciones.all():
                valor_seleccionado = request.POST.get(opcion.nombre)
                if not valor_seleccionado:
                    return JsonResponse({
                        'success': False,
                        'message': f'Por favor seleccione {opcion.nombre}'
                    })
                
                # Buscar el precio de la opción seleccionada
                for opcion_item in opcion.opciones:
                    if opcion_item['valor'] == valor_seleccionado:
                        precio_total = float(opcion_item.get('precio', 0))
                        break
                
                opciones[opcion.nombre] = {
                    'valor': valor_seleccionado,
                    'precio': precio_total
                }

            # Crear el item del carrito con el precio
            item_carrito = ItemCarrito.objects.create(
                carrito=carrito,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=precio_total,  # Guardar el precio unitario
                opciones=opciones
            )

            return JsonResponse({
                'success': True,
                'message': 'Producto agregado al carrito',
                'redirect_url': reverse('carrito')
            })

        except ValueError as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
        except Exception as e:
            print(f"Error: {str(e)}")  # Para debugging
            return JsonResponse({
                'success': False,
                'message': 'Error al procesar la solicitud'
            })

    return JsonResponse({
        'success': False,
        'message': 'Método no permitido'
    })



@login_required
def carrito(request):
    """Ver el contenido del carrito"""
    try:
        carrito = Carrito.objects.get(usuario=request.user)
        return render(request, 'contacto/carrito.html', {
            'carrito': carrito,
            'items': carrito.itemcarrito_set.select_related('producto').all()
        })
    except Carrito.DoesNotExist:
        messages.warning(request, 'No tienes productos en el carrito')
        return redirect('tienda')
    

@login_required
def ver_carrito(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.itemcarrito_set.all().select_related('producto').order_by('fecha_agregado')
    total = sum(item.subtotal for item in items)
    
    # Formatear los valores con puntos como separadores de miles
    for item in items:
        item.subtotal_formateado = f"${item.subtotal:,.0f} COP".replace(",", ".")
        item.precio_unitario_formateado = f"${item.precio_unitario:,.0f} COP".replace(",", ".")

    
    total_formateado = f"${total:,.0f} COP".replace(",", ".")
    
    context = {
        'items': items,
        'total': total,
        'total_formateado': total_formateado
    }
    
    return render(request, 'contacto/carrito.html', context)


@login_required
def pagar(request):
    """Procesar el pago del carrito"""
    carrito = get_object_or_404(Carrito, usuario=request.user)
    
    if not carrito.itemcarrito_set.exists():
        messages.error(request, 'Tu carrito está vacío')
        return redirect('carrito')

    try:
        # Aquí iría la lógica de pago con PayPal, Binance, etc.
        pedido = Pedido.objects.create(
            usuario=request.user,
            total=carrito.total(),
            metodo_pago='pendiente'  # Actualizar según el método seleccionado
        )

        # Transferir items del carrito al pedido
        for item in carrito.itemcarrito_set.all():
            ItemPedido.objects.create(
                pedido=pedido,
                producto=item.producto,
                cantidad=item.cantidad,
                opciones=item.opciones
            )

        # Limpiar el carrito
        carrito.itemcarrito_set.all().delete()
        
        messages.success(request, 'Pedido realizado con éxito')
        return redirect('gracias')

    except Exception as e:
        messages.error(request, f'Error al procesar el pago: {str(e)}')
        return redirect('carrito')

@login_required
def eliminar_del_carrito(request, item_id):
    """Eliminar un item del carrito"""
    if request.method == 'POST':
        item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
        item.delete()
        return JsonResponse({'success': True, 'message': 'Producto eliminado del carrito'})
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@login_required
def actualizar_cantidad(request, item_id):
    """Actualizar la cantidad de un item en el carrito"""
    if request.method == 'POST':
        item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
        cantidad = request.POST.get('cantidad')
        
        try:
            cantidad = int(cantidad)
            if cantidad > 0:
                item.cantidad = cantidad
                item.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Cantidad actualizada',
                    'nuevo_subtotal': float(item.subtotal)  # Acceso a la propiedad, sin paréntesis
                })
        except ValueError:
            return JsonResponse({'success': False, 'message': 'Cantidad inválida'})
        
    return JsonResponse({'success': False, 'message': 'Método no permitido'})




# Función para manejar el formulario de contacto sin plantilla específica
def enviar_mensaje(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido') 
        correo = request.POST.get('correo')
        mensaje = request.POST.get('mensaje')

        try:
            # Obtener la fecha y hora actual en Bogotá
            bogota_tz = pytz.timezone('America/Bogota')
            fecha_actual = timezone.now().astimezone(bogota_tz).strftime('%d/%m/%Y %I:%M:%S %p')

            # Formatear el cuerpo del mensaje
            cuerpo_mensaje = f"""
            Ha recibido un nuevo mensaje de contacto:

            Nombre: {nombre} {apellido}
            Correo: {correo}

            Fecha y hora del mensaje: {fecha_actual}

            Mensaje:
            {mensaje}
            """

            # Enviar correo al administrador
            send_mail(
                subject=f'Nuevo mensaje de {nombre} {apellido}',
                message=cuerpo_mensaje,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_ADMIN],  # Correo del admin
                fail_silently=False,
            )

            mensaje_confirmacion = f"""
            Hola {nombre},

            Hemos recibido su mensaje y pronto nos contactaremos con usted.

            ¡Gracias por ponerse en contacto con nosotros!

            Mensaje recibido el {fecha_actual}

            Atentamente,
            El equipo de J Silva Ingeniería.
            """

            # Enviar correo de confirmación al usuario
            send_mail(
                subject='Confirmación de recepción de mensaje',
                message=mensaje_confirmacion,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[correo],  # Correo del cliente
                fail_silently=False,
            )

            # Guardar el mensaje en la base de datos
            nuevo_mensaje = Mensaje(
                nombre=nombre,
                apellido=apellido,
                correo=correo,
                mensaje=mensaje
            )
            nuevo_mensaje.save()

            # Retornar JSON con 'success' para mostrar la notificación de éxito
            return JsonResponse({'success': True, 'message': "Mensaje enviado correctamente."})
        
        except Exception as e:
            # Loguear el error si es necesario (opcional)
            print(f"Error al enviar el mensaje: {e}")
            # Retornar JSON con 'success: False' para mostrar error
            return JsonResponse({'success': False, 'message': "Error al enviar el mensaje. Inténtalo de nuevo más tarde."})
    
    return JsonResponse({'success': False, 'message': "Método no permitido."})
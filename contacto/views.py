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
from .forms import ProductoForm
from .models import HistorialCompra, HistorialReserva


import os

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
    Producto
)
from .utils import enviar_correo_confirmacion, validar_fecha_hora

# Obtener el modelo de usuario personalizado
User = get_user_model()




def crear_superusuario(request):
    User = get_user_model()
    email = 'admin@admin.com'
    password = 'admin123'

    if not User.objects.filter(email=email).exists():
        User.objects.create_superuser(
            email=email,
            username='admin',
            password=password,
        )
        return HttpResponse('Superusuario creado correctamente ✅')
    else:
        user = User.objects.get(email=email)
        # Asegurar que sea superuser y staff
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return HttpResponse('El usuario ya existía. Se actualizó como superusuario 👍')


def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)  # OJO: request.FILES es necesario para imágenes
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado con éxito.')
            return redirect('lista_productos')  # Ajusta esto según tu proyecto
    else:
        form = ProductoForm()
    
    return render(request, 'crear_producto.html', {'form': form})



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
    # Si es GET, mostrar la página de login
    if request.method == 'GET':
        return render(request, 'contacto/login.html')
        
    # Si es POST, procesar el inicio de sesión
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        
        # Validación básica
        if not email or not password:
            return JsonResponse({
                'success': False,
                'message': 'Por favor, complete todos los campos.'
            })
        
        # Intentar autenticar al usuario
        try:
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                return JsonResponse({
                    'success': True,
                    'message': 'Inicio de sesión exitoso.',
                    'redirect_url': reverse('contacto:inicio')
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Credenciales incorrectas. Por favor, verifique su correo y contraseña.'
                })
                
        except Exception as e:
            print(f"Error en login_view: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': 'Ocurrió un error en el servidor. Por favor, intente nuevamente más tarde.'
            })
    
    # Si llega aquí, el método no está permitido
    return JsonResponse({
        'success': False,
        'message': 'Método no permitido'
    })

# Función registrarse
def register_view(request):
    # Solo aceptamos método POST para registro
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'message': 'Método no permitido'
        })
    
    # Obtener datos del formulario
    try:
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        
        # Validaciones
        if not all([first_name, last_name, email, password1, password2]):
            return JsonResponse({
                'success': False,
                'message': 'Por favor, complete todos los campos.'
            })
            
        if password1 != password2:
            return JsonResponse({
                'success': False,
                'message': 'Las contraseñas no coinciden.'
            })
            
        if len(password1) < 6:
            return JsonResponse({
                'success': False,
                'message': 'La contraseña debe tener al menos 6 caracteres.'
            })
            
        # Verificar si el correo ya existe
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'success': False,
                'message': 'Este correo electrónico ya está registrado.'
            })
            
        # Crear usuario
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )
        
        # Iniciar sesión automáticamente
        login(request, user)
        
        return JsonResponse({
            'success': True,
            'message': 'Registro exitoso. Bienvenido/a a J Silva Ingeniería.',
            'redirect_url': reverse('contacto:inicio')
        })
        
    except Exception as e:
        print(f"Error en register_view: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': 'Ocurrió un error en el servidor. Por favor, intente nuevamente más tarde.'
        })

# Función cerrar sesión
def logout_view(request):
    logout(request)
    return redirect('contacto:inicio')

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

@login_required
def historial_compras_reservas(request):
    compras = HistorialCompra.objects.filter(usuario=request.user)
    reservas = HistorialReserva.objects.filter(usuario=request.user)
    return render(request, 'contacto/historial-pedidos.html', {'compras': compras, 'reservas': reservas})
from django import forms
from .models import Reserva, Mensaje, Servicio
from .utils import enviar_correo_confirmacion, validar_fecha_hora
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.forms import SetPasswordForm
from .models import Producto



# Contraseñas recuperar
class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={'class': 'input', 'placeholder': 'Correo electrónico'}),
    )

class PasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Nueva contraseña'}),
    )
    new_password2 = forms.CharField(
        label="Confirmar nueva contraseña",
        widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Confirmar nueva contraseña'}),
    )




# Formulario de Reserva
class ReservaForm(forms.ModelForm):
    servicio = forms.ModelChoiceField(queryset=Servicio.objects.all(), label="Servicio")
    fecha_hora = forms.DateTimeField(required=True, label="Fecha y Hora", widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    numero_celular = forms.CharField(max_length=15, required=True, label="Número de celular")
    numero_celular = forms.CharField(max_length=15, required=True, label="Número de celular")
    direccion = forms.CharField(max_length=255, required=True, label="Dirección")
    ciudad = forms.CharField(max_length=100, required=True, label="Ciudad")


    # Desinfección
    tipo_lugar = forms.ChoiceField(choices=[('residencial', 'Residencial'), ('comercial', 'Comercial'), ('industrial', 'Industrial')], required=False, label="Tipo de lugar")
    area = forms.DecimalField(required=False, label="Área en metros cuadrados")
    tipo_plaga = forms.ChoiceField(choices=[('insectos', 'Insectos'), ('roedores', 'Roedores'), ('otros', 'Otros')], required=False, label="Tipo de plaga")
    plaga_detalle = forms.CharField(required=False, label="Detalles de la plaga", widget=forms.Textarea)
    desinfeccion_previa = forms.ChoiceField(choices=[('si', 'Sí'), ('no', 'No')], required=False, label="¿Se ha realizado desinfección previamente?")
    productos_preferidos = forms.CharField(required=False, label="Productos específicos", widget=forms.Textarea)

    # Control Apícola
    ubicacion_colmena = forms.ChoiceField(choices=[('interior', 'Interior'), ('exterior', 'Exterior')], required=False, label="Ubicación de la colmena")
    accesibilidad = forms.ChoiceField(choices=[('facil', 'Fácil'), ('dificil', 'Difícil')], required=False, label="Accesibilidad")
    cantidad_colmenas = forms.IntegerField(required=False, label="Cantidad aproximada de colmenas")
    abejas_agresivas = forms.ChoiceField(choices=[('si', 'Sí'), ('no', 'No')], required=False, label="¿Las abejas han mostrado agresividad?")
    tratamiento_abejas = forms.ChoiceField(choices=[('reubicacion', 'Reubicación'), ('eliminacion', 'Eliminación')], required=False, label="Tratamiento preferido")

    # Jardinería
    tipo_servicio_jardineria = forms.ChoiceField(choices=[('mantenimiento', 'Mantenimiento'), ('diseno', 'Diseño de jardín'), ('poda', 'Poda'), ('riego', 'Sistema de riego')], required=False, label="Tipo de servicio")
    area_jardin = forms.DecimalField(required=False, label="Tamaño del jardín (en metros cuadrados)")
    frecuencia_mantenimiento = forms.ChoiceField(choices=[('semanal', 'Semanal'), ('quincenal', 'Quincenal'), ('mensual', 'Mensual'), ('unica', 'Única vez')], required=False, label="Frecuencia de mantenimiento")
    plantas_especificas = forms.CharField(required=False, label="Plantas específicas", widget=forms.Textarea)
    riego_instalado = forms.ChoiceField(choices=[('si', 'Sí'), ('no', 'No')], required=False, label="¿Sistema de riego instalado?")
    
    # Capacitación
    tipo_capacitacion = forms.ChoiceField(choices=[('prevencion', 'Prevención de incendios'), ('saneamiento', 'Saneamiento básico'), ('seguridad', 'Seguridad laboral')], required=False, label="Tipo de capacitación")
    numero_personas = forms.IntegerField(required=False, label="Número de personas a capacitar")
    capacitacion_presencial = forms.ChoiceField(choices=[('presencial', 'Presencial'), ('virtual', 'Virtual')], required=False, label="Ubicación de la capacitación")
    certificacion = forms.ChoiceField(choices=[('si', 'Sí'), ('no', 'No')], required=False, label="¿Requiere certificación oficial?")

    class Meta:
        model = Reserva
        fields = ['servicio', 'fecha_hora', 'numero_celular', 'direccion', 'ciudad']

    def clean(self):
        cleaned_data = super().clean()
        servicio = cleaned_data.get('servicio')
        fecha_hora = cleaned_data.get('fecha_hora')

        # Verificar que el servicio esté seleccionado
        if not servicio:
            self.add_error('servicio', 'Debe seleccionar un servicio.')

        # Verificar que fecha_hora no sea None
        if fecha_hora is None:
            self.add_error('fecha_hora', 'La fecha y hora de la reserva no pueden estar vacías.')

        # Validaciones específicas por servicio
        if servicio:
            servicio_nombre = servicio.servicio_nombre.lower()  # Convertir el nombre del servicio a minúsculas

            if servicio_nombre == 'desinfeccion':
                if not cleaned_data.get('tipo_lugar'):
                    self.add_error('tipo_lugar', 'Este campo es obligatorio para desinfección.')
                if not cleaned_data.get('area'):
                    self.add_error('area', 'Este campo es obligatorio para desinfección.')
            elif servicio_nombre == 'control_apicola':
                if not cleaned_data.get('ubicacion_colmena'):
                    self.add_error('ubicacion_colmena', 'Este campo es obligatorio para control apícola.')
                if not cleaned_data.get('cantidad_colmenas'):
                    self.add_error('cantidad_colmenas', 'Este campo es obligatorio para control apícola.')
            elif servicio_nombre == 'jardineria':
                if not cleaned_data.get('tipo_servicio_jardineria'):
                    self.add_error('tipo_servicio_jardineria', 'Este campo es obligatorio para jardinería.')
            elif servicio_nombre == 'capacitacion':
                if not cleaned_data.get('tipo_capacitacion'):
                    self.add_error('tipo_capacitacion', 'Este campo es obligatorio para capacitación.')


        return cleaned_data

# Formulario de Producto
class ExtintorForm(forms.Form):
    OPCIONES_EXTINTOR = [
        ('compra', 'Comprar'),
        ('mantenimiento', 'Mantenimiento'),
    ]
    TIPOS_EXTINTOR = [
        ('polvo_quimico', 'Polvo químico'),
        ('co2', 'CO2'),
        ('agua', 'Agua'),
    ]

    opcion = forms.ChoiceField(choices=OPCIONES_EXTINTOR, widget=forms.RadioSelect)
    tipo = forms.ChoiceField(choices=TIPOS_EXTINTOR)
    cantidad = forms.IntegerField(min_value=1)

class Plano3DForm(forms.Form):
    TIPOS_PLANO = [
        ('residencial', 'Residencial'),
        ('comercial', 'Comercial'),
        ('industrial', 'Industrial'),
    ]
    ESCALAS_PLANO = [
        ('1:50', '1:50'),
        ('1:100', '1:100'),
        ('1:200', '1:200'),
    ]

    tipo = forms.ChoiceField(choices=TIPOS_PLANO)
    escala = forms.ChoiceField(choices=ESCALAS_PLANO)
    cantidad = forms.IntegerField(min_value=1)




# Formulario de Mensaje
class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['nombre', 'apellido', 'correo', 'mensaje']
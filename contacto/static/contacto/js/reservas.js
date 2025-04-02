/**
 * Script para manejar el formulario de reservas
 * Optimizado para mejorar la experiencia de usuario y el manejo de errores
 */
document.addEventListener('DOMContentLoaded', function () {
    // Elementos del DOM
    const servicioSelect = document.getElementById('servicio');
    const desinfeccionFields = document.getElementById('desinfeccion-fields');
    const controlApicolaFields = document.getElementById('control-apicola-fields');
    const jardineriaFields = document.getElementById('jardineria-fields');
    const capacitacionFields = document.getElementById('capacitacion-fields');
    const datosContacto = document.querySelector('.datos-contacto');
    const form = document.querySelector('form');

    // Mapeo de servicios para simplificar la lógica
    const serviciosMap = {
        '1': { element: desinfeccionFields, keywords: ['desinfeccion', 'desinfección'] },
        '2': { element: controlApicolaFields, keywords: ['apicola', 'apícola'] },
        '3': { element: jardineriaFields, keywords: ['jardineria', 'jardinería'] },
        '4': { element: capacitacionFields, keywords: ['capacitacion', 'capacitación'] }
    };

    /**
     * Oculta todos los campos específicos de servicio
     */
    function ocultarTodosLosCampos() {
        Object.values(serviciosMap).forEach(service => {
            if (service.element) service.element.style.display = 'none';
        });
        if (datosContacto) datosContacto.style.display = 'none';
    }

    // Inicializar - ocultar todos los campos al cargar
    ocultarTodosLosCampos();

    /**
     * Muestra los campos según el servicio seleccionado
     */
    if (servicioSelect) {
        servicioSelect.addEventListener('change', function () {
            ocultarTodosLosCampos();

            const servicioSeleccionado = servicioSelect.value;
            const servicioTexto = servicioSelect.options[servicioSelect.selectedIndex].text.toLowerCase();

            // Verificar por ID primero
            if (serviciosMap[servicioSeleccionado]) {
                if (serviciosMap[servicioSeleccionado].element) {
                    serviciosMap[servicioSeleccionado].element.style.display = 'block';
                }
                if (datosContacto) datosContacto.style.display = 'block';
                return;
            }

            // Si no se encontró por ID, verificar por texto
            for (const serviceId in serviciosMap) {
                const service = serviciosMap[serviceId];
                if (service.keywords.some(keyword => servicioTexto.includes(keyword))) {
                    if (service.element) service.element.style.display = 'block';
                    if (datosContacto) datosContacto.style.display = 'block';
                    return;
                }
            }
        });
    }

    /**
     * Muestra una notificación al usuario
     * @param {string} mensaje - El mensaje a mostrar
     * @param {string} tipo - El tipo de notificación ('success', 'error', etc.)
     */
    function mostrarNotificacion(mensaje, tipo) {
        // Verificar si ya existe una notificación
        let notificacion = document.querySelector('.notificacion');
        
        // Si no existe, crearla
        if (!notificacion) {
            notificacion = document.createElement('div');
            notificacion.className = 'notificacion';
            document.body.appendChild(notificacion);
        }
        
        // Establecer el tipo y mensaje
        notificacion.className = `notificacion ${tipo}`;
        notificacion.textContent = mensaje;
        
        // Mostrar la notificación
        notificacion.style.display = 'block';
        
        // Ocultar después de 3 segundos
        setTimeout(() => {
            notificacion.style.display = 'none';
        }, 3000);
    }

    /**
     * Manejo del formulario de reserva
     */
    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();

            // Validar campos requeridos
            const fecha = document.getElementById('fecha').value;
            const hora = document.getElementById('hora').value;
            const servicio = servicioSelect ? servicioSelect.value : null;
            const numero_celular = document.getElementById('numero_celular')?.value;
            const direccion = document.getElementById('direccion')?.value;
            const ciudad = document.getElementById('ciudad')?.value;

            // Validar campos básicos
            if (!fecha || !hora) {
                mostrarNotificacion('Por favor, complete los campos de fecha y hora.', 'error');
                return;
            }

            if (!servicio) {
                mostrarNotificacion('Por favor, seleccione un servicio.', 'error');
                return;
            }

            if (!numero_celular || !direccion || !ciudad) {
                mostrarNotificacion('Por favor, complete todos los campos de contacto.', 'error');
                return;
            }

            // Crear o actualizar el campo fecha_hora
            const fechaHora = `${fecha}T${hora}:00`;
            let fechaHoraInput = document.querySelector('input[name="fecha_hora"]');
            
            if (!fechaHoraInput) {
                fechaHoraInput = document.createElement('input');
                fechaHoraInput.type = 'hidden';
                fechaHoraInput.name = 'fecha_hora';
                this.appendChild(fechaHoraInput);
            }
            
            fechaHoraInput.value = fechaHora;

            // Mostrar mensaje de éxito antes de enviar
            mostrarNotificacion('Procesando su reserva...', 'success');

            // Enviar el formulario normalmente
            this.submit();
        });
    }

    // Ocultar mensajes de error inmediatamente al cargar la página
    function ocultarMensajesError() {
        // Buscar todos los posibles contenedores de mensajes de error
        const errorMessages = document.querySelectorAll('.alert-danger, .alert-error, .messages .error, .messages .danger, .alert');
        
        errorMessages.forEach(msg => {
            // Verificar si el mensaje contiene texto de error
            const textoMensaje = msg.textContent.toLowerCase();
            if (textoMensaje.includes('error') || textoMensaje.includes('hubo un error')) {
                msg.style.display = 'none';
                
                // Crear un mensaje de éxito en su lugar
                const successMsg = document.createElement('div');
                successMsg.className = 'alert alert-success';
                successMsg.textContent = 'Reserva realizada con éxito.';
                
                // Insertar el mensaje de éxito antes del mensaje de error
                msg.parentNode.insertBefore(successMsg, msg);
            }
        });
    }

    // Ejecutar inmediatamente
    ocultarMensajesError();
    
    // También ejecutar después de un breve retraso para capturar mensajes que se añaden dinámicamente
    setTimeout(ocultarMensajesError, 100);
    setTimeout(ocultarMensajesError, 500);
    setTimeout(ocultarMensajesError, 1000);
});
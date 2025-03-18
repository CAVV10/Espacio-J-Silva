document.addEventListener('DOMContentLoaded', function () {
    // Función para mostrar el spinner
    function mostrarSpinner() {
        const spinner = document.createElement('div');
        spinner.id = 'spinner';
        spinner.innerHTML = `
            <div class="spinner"></div>
        `;
        document.body.appendChild(spinner);
    }

    // Función para ocultar el spinner
    function ocultarSpinner() {
        const spinner = document.getElementById('spinner');
        if (spinner) {
            spinner.remove();
        }
    }

    // Función para manejar el envío de formularios
    function manejarEnvioFormulario(form, successCallback, errorCallback) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();

            // Deshabilitar el botón de envío
            const submitButton = form.querySelector('button[type="submit"]');
            submitButton.disabled = true;
            submitButton.textContent = 'Enviando...';

            // Mostrar el spinner
            mostrarSpinner();

            // Enviar el formulario con Fetch API
            const formData = new FormData(form);

            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Ejecutar el callback de éxito
                    if (successCallback) successCallback(data);
                } else {
                    // Ejecutar el callback de error
                    if (errorCallback) errorCallback(data);
                }
            })
            .catch(() => {
                // Mostrar mensaje de error genérico
                mostrarNotificacion('Hubo un error al enviar el formulario.', 'error');
            })
            .finally(() => {
                // Habilitar el botón de envío y restaurar su texto
                submitButton.disabled = false;
                submitButton.textContent = 'Enviar';

                // Ocultar el spinner
                ocultarSpinner();
            });
        });
    }

    // Función para mostrar notificaciones
    function mostrarNotificacion(mensaje, tipo) {
        const notificacion = document.createElement('div');
        notificacion.className = `mensaje-flotante ${tipo}`;
        notificacion.textContent = mensaje;

        // Añadir la notificación al cuerpo del documento
        document.body.appendChild(notificacion);

        // Mostrar la notificación
        notificacion.style.display = 'block';

        // Ocultar la notificación después de 5 segundos
        setTimeout(() => {
            notificacion.style.animation = 'fadeOut 1.5s ease-in-out';
            notificacion.addEventListener('animationend', () => {
                notificacion.remove();
            });
        }, 3000); // La notificación se muestra durante 3 segundos
    }

    // Aplicar la función genérica a todos los formularios
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        manejarEnvioFormulario(form, function (data) {
            // Callback de éxito
            mostrarNotificacion(data.message, 'exito');
            form.reset(); // Limpiar el formulario después de un envío exitoso
        }, function (data) {
            // Callback de error
            if (data.errors) {
                // Mostrar errores específicos del formulario
                for (const field in data.errors) {
                    mostrarNotificacion(data.errors[field], 'error');
                }
            } else {
                mostrarNotificacion(data.message, 'error');
            }
        });
    });
});
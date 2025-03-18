document.addEventListener('DOMContentLoaded', function() {
    // Deshabilitar TODA validación nativa del navegador
    document.addEventListener('invalid', (function(){
        return function(e) {
            e.preventDefault();
            e.stopPropagation();
        };
    })(), true);
    
    // Remover atributos required y validación HTML5
    document.querySelectorAll('form').forEach(form => {
        form.setAttribute('novalidate', 'true'); // Deshabilitar validación nativa
        form.querySelectorAll('[required], [pattern], [min], [max], [minlength], [maxlength]').forEach(field => {
            field.removeAttribute('required');
            field.removeAttribute('pattern');
            field.removeAttribute('min');
            field.removeAttribute('max');
            field.removeAttribute('minlength');
            field.removeAttribute('maxlength');
        });
    });

    // Asegurarse de que los modales estén ocultos al cargar
    document.querySelectorAll('.modal').forEach(modal => {
        modal.style.display = 'none';
    });

    // Función para mostrar mensaje personalizado
    function mostrarMensaje(mensaje, tipo = 'success') {
        // Remover mensajes anteriores del mismo tipo
        document.querySelectorAll(`.mensaje-${tipo}`).forEach(msg => msg.remove());
        
        const mensajeDiv = document.createElement('div');
        mensajeDiv.className = `mensaje-${tipo}`;
        mensajeDiv.textContent = mensaje;
        document.body.appendChild(mensajeDiv);
        
        setTimeout(() => {
            mensajeDiv.remove();
        }, 3000);
    }

    // Función para calcular y actualizar el precio total
    function actualizarPrecioTotal(form) {
        const precioBase = parseFloat(form.querySelector('.precio-base').dataset.precio);
        const cantidad = parseInt(form.querySelector('input[name="cantidad"]').value) || 1;
        let precioTotal = precioBase;

        // Sumar precios de opciones seleccionadas
        form.querySelectorAll('select').forEach(select => {
            const opcionSeleccionada = select.options[select.selectedIndex];
            if (opcionSeleccionada && opcionSeleccionada.dataset.precio) {
                precioTotal += parseFloat(opcionSeleccionada.dataset.precio);
            }
        });

        // Multiplicar por cantidad
        precioTotal *= cantidad;

        // Actualizar el precio total en el formulario
        const precioElement = form.querySelector('.precio-total span');
        if (precioElement) {
            precioElement.textContent = precioTotal.toLocaleString('es-CO');
        }
    }

    // Función para cerrar todos los modales
    function cerrarModales() {
        document.querySelectorAll('.modal').forEach(modal => {
            modal.style.display = 'none';
        });
    }

    // Manejar formularios de productos
    document.querySelectorAll('.form-producto').forEach(form => {
        // Prevenir validación por defecto
        form.addEventListener('invalid', (e) => {
            e.preventDefault();
        }, true);

        // Inicializar precio total
        actualizarPrecioTotal(form);

        // Escuchar cambios en selects (opciones)
        form.querySelectorAll('select').forEach(select => {
            select.addEventListener('change', () => {
                select.classList.remove('invalid');
                actualizarPrecioTotal(form);
            });
        });

        // Escuchar cambios en cantidad
        const inputCantidad = form.querySelector('input[name="cantidad"]');
        if (inputCantidad) {
            ['change', 'input'].forEach(evento => {
                inputCantidad.addEventListener(evento, () => {
                    if (inputCantidad.value < 1) inputCantidad.value = 1;
                    actualizarPrecioTotal(form);
                });
            });
        }

        // Manejar envío del formulario
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            e.stopPropagation();
            e.stopImmediatePropagation();

            // Limpiar cualquier mensaje o estado previo
            document.querySelectorAll('[class^="mensaje-"]').forEach(msg => msg.remove());
            this.querySelectorAll('.invalid').forEach(el => el.classList.remove('invalid'));

            // Validación manual
            const selects = this.querySelectorAll('select');
            let todosLosCamposValidos = true;
            let primerError = null;

            for (const select of selects) {
                if (!select.value) {
                    todosLosCamposValidos = false;
                    select.classList.add('invalid');
                    if (!primerError) {
                        primerError = select;
                        mostrarMensaje(`Por favor seleccione ${select.getAttribute('name')}`, 'error');
                    }
                }
            }

            if (!todosLosCamposValidos) {
                primerError.focus();
                return false;
            }

            // Continuar con el envío si todo es válido
            try {
                const formData = new FormData(this);
                const response = await fetch(`/agregar-al-carrito/${formData.get('producto_id')}/`, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                    }
                });

                const data = await response.json();
                
                if (data.success) {
                    cerrarModales();
                    this.reset();
                    actualizarPrecioTotal(this);
                    mostrarMensaje('Producto agregado al carrito');
                    
                    if (data.redirect_url) {
                        setTimeout(() => {
                            window.location.href = data.redirect_url;
                        }, 1500);
                    }
                } else {
                    mostrarMensaje(data.message || 'Error al agregar al carrito', 'error');
                }
            } catch (error) {
                console.error('Error:', error);
                mostrarMensaje('Error al procesar la solicitud', 'error');
            }
        });
    });

    // Manejar botones de comprar
    document.querySelectorAll('.btn-comprar').forEach(boton => {
        boton.addEventListener('click', function() {
            cerrarModales();
            const productoId = this.dataset.productoId;
            const tipo = this.closest('.producto').dataset.tipo;
            const modal = document.getElementById(`modal-${tipo}-${productoId}`);
            if (modal) {
                modal.style.display = 'flex';
                modal.style.alignItems = 'center';
                modal.style.justifyContent = 'center';
            }
        });
    });

    // Cerrar modales con botón X
    document.querySelectorAll('.close').forEach(closeBtn => {
        closeBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            const modal = this.closest('.modal');
            if (modal) {
                modal.style.display = 'none';
            }
        });
    });

    // Cerrar modal al hacer clic fuera
    window.addEventListener('click', function(event) {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = 'none';
        }
    });

    // Prevenir que el clic en el contenido del modal lo cierre
    document.querySelectorAll('.modal-content').forEach(content => {
        content.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    });
});
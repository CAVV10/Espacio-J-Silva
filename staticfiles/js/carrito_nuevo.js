// Script simplificado para el carrito de compras
document.addEventListener('DOMContentLoaded', function() {
    console.log('carrito_nuevo.js cargado');

    // Obtener CSRF token
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    console.log('CSRF token encontrado:', csrfToken ? 'Sí' : 'No');

    // 1. Botones de disminuir cantidad (usar la clase específica)
    const botonesDecrementar = document.querySelectorAll('.btn-decrementar');
    console.log('Botones decrementar encontrados:', botonesDecrementar.length);
    
    botonesDecrementar.forEach(boton => {
        const itemId = boton.getAttribute('data-item-id');
        console.log('Configurando botón decrementar para item:', itemId);
        
        boton.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Click en botón decrementar:', itemId);
            
            // Encontrar el span de cantidad
            const cantidadElement = this.nextElementSibling;
            if (!cantidadElement) {
                console.error('No se encontró el elemento de cantidad');
                return;
            }
            
            const cantidad = parseInt(cantidadElement.textContent);
            if (cantidad <= 1) {
                alert('La cantidad mínima es 1');
                return;
            }
            
            const nuevaCantidad = cantidad - 1;
            actualizarCantidadEnServidor(itemId, nuevaCantidad, cantidadElement);
        });
    });

    // 2. Botones de aumentar cantidad
    const botonesIncrementar = document.querySelectorAll('.btn-incrementar');
    console.log('Botones incrementar encontrados:', botonesIncrementar.length);
    
    botonesIncrementar.forEach(boton => {
        const itemId = boton.getAttribute('data-item-id');
        console.log('Configurando botón incrementar para item:', itemId);
        
        boton.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Click en botón incrementar:', itemId);
            
            // Encontrar el span de cantidad
            const cantidadElement = this.previousElementSibling;
            if (!cantidadElement) {
                console.error('No se encontró el elemento de cantidad');
                return;
            }
            
            const cantidad = parseInt(cantidadElement.textContent);
            const nuevaCantidad = cantidad + 1;
            actualizarCantidadEnServidor(itemId, nuevaCantidad, cantidadElement);
        });
    });

    // 3. Botones de eliminar producto
    const botonesEliminar = document.querySelectorAll('.btn-eliminar');
    console.log('Botones eliminar encontrados:', botonesEliminar.length);
    
    botonesEliminar.forEach(boton => {
        const itemId = boton.getAttribute('data-item-id');
        console.log('Configurando botón eliminar para item:', itemId);
        
        boton.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Click en botón eliminar:', itemId);
            
            if (confirm('¿Está seguro de eliminar este producto del carrito?')) {
                eliminarProducto(itemId, this);
            }
        });
    });

    // Función para actualizar cantidad en el servidor
    function actualizarCantidadEnServidor(itemId, nuevaCantidad, cantidadElement) {
        // Crear datos del formulario
        const formData = new FormData();
        formData.append('cantidad', nuevaCantidad);

        // Realizar petición AJAX
        fetch(`/carrito/actualizar/${itemId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: new URLSearchParams(formData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la respuesta del servidor: ' + response.status);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Actualizar la UI
                cantidadElement.textContent = nuevaCantidad;
                
                // Actualizar el subtotal
                const fila = cantidadElement.closest('tr');
                const subtotalElement = fila.querySelector('td:nth-child(4) p');
                if (subtotalElement) {
                    subtotalElement.textContent = data.nuevo_subtotal_formateado;
                }
                
                // Actualizar el total
                const totalElement = document.querySelector('.text-gray-900.dark\\:text-white.font-bold.text-xl');
                if (totalElement && data.nuevo_total_formateado) {
                    totalElement.textContent = data.nuevo_total_formateado;
                }
                
                console.log('Cantidad actualizada con éxito');
            } else {
                alert(data.message || 'Error al actualizar la cantidad');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Ocurrió un error al actualizar la cantidad');
        });
    }

    // Función para eliminar producto
    function eliminarProducto(itemId, botonEliminar) {
        fetch(`/carrito/eliminar/${itemId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la respuesta del servidor: ' + response.status);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Eliminar la fila
                const fila = botonEliminar.closest('tr');
                if (fila) {
                    fila.remove();
                }
                
                // Actualizar el total
                const totalElement = document.querySelector('.text-gray-900.dark\\:text-white.font-bold.text-xl');
                if (totalElement && data.nuevo_total_formateado) {
                    totalElement.textContent = data.nuevo_total_formateado;
                }
                
                // Si no hay más productos, mostrar mensaje
                const filas = document.querySelectorAll('tbody tr');
                if (filas.length === 0) {
                    const tbody = document.querySelector('tbody');
                    if (tbody) {
                        const emptyRow = document.createElement('tr');
                        emptyRow.innerHTML = '<td colspan="5" class="py-4 px-4 text-center text-gray-600 dark:text-gray-400">Tu carrito está vacío</td>';
                        tbody.appendChild(emptyRow);
                    }
                }
                
                console.log('Producto eliminado con éxito');
            } else {
                alert(data.message || 'Error al eliminar el producto');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Ocurrió un error al eliminar el producto');
        });
    }

    // Configuración de botones adicionales si existen
    const btnPagar = document.getElementById('btn-pagar');
    if (btnPagar) {
        btnPagar.addEventListener('click', function() {
            const modalNequi = document.getElementById('modal-nequi');
            if (modalNequi) {
                modalNequi.classList.remove('hidden');
            }
        });
    }

    // Configurar botones para cerrar modales
    document.querySelectorAll('.close').forEach(btn => {
        btn.addEventListener('click', function() {
            const modal = this.closest('#modal-nequi');
            if (modal) {
                modal.classList.add('hidden');
            }
        });
    });
});

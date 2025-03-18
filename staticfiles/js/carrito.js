document.addEventListener('DOMContentLoaded', function() {
    console.log('Carrito JS cargado');

    // Obtener token CSRF
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    if (!csrfToken) console.error('No se pudo encontrar el token CSRF');

    // Función para hacer peticiones AJAX
    async function fetchData(url, method, body) {
        try {
            const response = await fetch(url, {
                method: method,
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: body
            });
            
            if (!response.ok) throw new Error(`Error del servidor: ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('Error en petición:', error);
            alert('Error en la operación: ' + error.message);
            throw error;
        }
    }

    // Actualizar el total del carrito
    function actualizarTotal(total) {
        const totalElement = document.querySelector('.text-gray-900.dark\\:text-white.font-bold.text-xl');
        if (totalElement) {
            totalElement.textContent = total;
        }
    }

    // ASIGNAR EVENTOS A LOS BOTONES DE INCREMENTAR (+)
    const botonesIncrementar = document.querySelectorAll('button[data-item-id]');
    botonesIncrementar.forEach(function(boton) {
        // Verificar si el botón contiene un SVG con el símbolo +
        if (boton.innerHTML.includes('M7 2.33331V11.6666M2.33333 7H11.6667')) {
            const itemId = boton.getAttribute('data-item-id');
            
            boton.addEventListener('click', async function(e) {
                e.preventDefault();
                
                // Encontrar el span de cantidad (hermano adyacente)
                const cantidadElement = this.parentNode.querySelector('span');
                if (!cantidadElement) return;
                
                const cantidad = parseInt(cantidadElement.textContent);
                const nuevaCantidad = cantidad + 1;
                
                try {
                    const data = await fetchData(
                        `/carrito/actualizar/${itemId}/`, 
                        'POST', 
                        `cantidad=${nuevaCantidad}`
                    );
                    
                    if (data.success) {
                        // Actualizar cantidad en UI
                        cantidadElement.textContent = nuevaCantidad;
                        
                        // Actualizar subtotal de línea
                        const row = this.closest('tr');
                        const subtotalElement = row.querySelector('td:nth-child(4) p');
                        if (subtotalElement) {
                            subtotalElement.textContent = data.nuevo_subtotal_formateado;
                        }
                        
                        // Actualizar total
                        if (data.nuevo_total_formateado) {
                            actualizarTotal(data.nuevo_total_formateado);
                        }
                    } else {
                        alert(data.message || "Error al actualizar cantidad");
                    }
                } catch (error) {
                    console.error('Error:', error);
                }
            });
        }
    });

    // ASIGNAR EVENTOS A LOS BOTONES DE DECREMENTAR (-)
    const botonesDecrementar = document.querySelectorAll('button[data-item-id]');
    botonesDecrementar.forEach(function(boton) {
        // Verificar si el botón contiene un SVG con el símbolo -
        if (boton.innerHTML.includes('M2.33398 7H11.6673')) {
            const itemId = boton.getAttribute('data-item-id');
            
            boton.addEventListener('click', async function(e) {
                e.preventDefault();
                
                // Encontrar el span de cantidad (hermano adyacente)
                const cantidadElement = this.parentNode.querySelector('span');
                if (!cantidadElement) return;
                
                const cantidad = parseInt(cantidadElement.textContent);
                if (cantidad <= 1) {
                    alert('La cantidad mínima es 1');
                    return;
                }
                
                const nuevaCantidad = cantidad - 1;
                
                try {
                    const data = await fetchData(
                        `/carrito/actualizar/${itemId}/`, 
                        'POST', 
                        `cantidad=${nuevaCantidad}`
                    );
                    
                    if (data.success) {
                        // Actualizar cantidad en UI
                        cantidadElement.textContent = nuevaCantidad;
                        
                        // Actualizar subtotal de línea
                        const row = this.closest('tr');
                        const subtotalElement = row.querySelector('td:nth-child(4) p');
                        if (subtotalElement) {
                            subtotalElement.textContent = data.nuevo_subtotal_formateado;
                        }
                        
                        // Actualizar total
                        if (data.nuevo_total_formateado) {
                            actualizarTotal(data.nuevo_total_formateado);
                        }
                    } else {
                        alert(data.message || "Error al actualizar cantidad");
                    }
                } catch (error) {
                    console.error('Error:', error);
                }
            });
        }
    });

    // ASIGNAR EVENTOS A LOS BOTONES DE ELIMINAR (X)
    const botonesEliminar = document.querySelectorAll('.text-gray-400.hover\\:text-red-500 button');
    botonesEliminar.forEach(function(boton) {
        const itemId = boton.getAttribute('data-item-id');
        if (!itemId) return;
        
        boton.addEventListener('click', async function(e) {
            e.preventDefault();
            
            if (confirm('¿Está seguro de eliminar este producto del carrito?')) {
                try {
                    const data = await fetchData(`/carrito/eliminar/${itemId}/`, 'POST');
                    
                    if (data.success) {
                        // Eliminar fila
                        const row = this.closest('tr');
                        if (row) row.remove();
                        
                        // Actualizar total
                        if (data.nuevo_total_formateado) {
                            actualizarTotal(data.nuevo_total_formateado);
                        }
                        
                        // Si no hay más filas, mostrar mensaje de carrito vacío
                        const filas = document.querySelectorAll('tbody tr');
                        if (filas.length === 0) {
                            const tbody = document.querySelector('tbody');
                            if (tbody) {
                                const emptyRow = document.createElement('tr');
                                emptyRow.innerHTML = '<td colspan="5" class="py-4 px-4 text-center text-gray-600 dark:text-gray-400">Tu carrito está vacío</td>';
                                tbody.appendChild(emptyRow);
                            }
                        }
                    } else {
                        alert(data.message || "Error al eliminar el producto");
                    }
                } catch (error) {
                    console.error('Error:', error);
                }
            }
        });
    });

    // Fallback: Asignar eventos a TODOS los botones con data-item-id
    if (botonesIncrementar.length === 0 || botonesDecrementar.length === 0) {
        console.log('Usando fallback para detectar botones');
        
        document.querySelectorAll('button[data-item-id]').forEach(function(boton) {
            const itemId = boton.getAttribute('data-item-id');
            
            // Determinar el tipo de botón basado en su ubicación y contenido
            if (boton.closest('.text-gray-400.hover\\:text-red-500')) {
                // Es botón de eliminar
                boton.addEventListener('click', async function(e) {
                    e.preventDefault();
                    
                    if (confirm('¿Está seguro de eliminar este producto del carrito?')) {
                        try {
                            const data = await fetchData(`/carrito/eliminar/${itemId}/`, 'POST');
                            
                            if (data.success) {
                                const row = this.closest('tr');
                                if (row) row.remove();
                                
                                if (data.nuevo_total_formateado) {
                                    actualizarTotal(data.nuevo_total_formateado);
                                }
                                
                                const filas = document.querySelectorAll('tbody tr');
                                if (filas.length === 0) {
                                    const tbody = document.querySelector('tbody');
                                    if (tbody) {
                                        const emptyRow = document.createElement('tr');
                                        emptyRow.innerHTML = '<td colspan="5" class="py-4 px-4 text-center text-gray-600 dark:text-gray-400">Tu carrito está vacío</td>';
                                        tbody.appendChild(emptyRow);
                                    }
                                }
                            } else {
                                alert(data.message || "Error al eliminar el producto");
                            }
                        } catch (error) {
                            console.error('Error:', error);
                        }
                    }
                });
            } else {
                // Es botón de + o -
                boton.addEventListener('click', function(e) {
                    e.preventDefault();
                    console.log('Click en botón:', boton.innerHTML);
                });
            }
        });
    }
});
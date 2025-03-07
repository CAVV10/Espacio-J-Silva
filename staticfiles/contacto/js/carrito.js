document.addEventListener('DOMContentLoaded', function() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Función para formatear números con puntos como separadores de miles
    function formatearNumero(numero) {
        return numero.toLocaleString('es-CO');
    }

    // Formatear los valores iniciales
    document.querySelectorAll('.subtotal').forEach(subtotalElement => {
        const subtotalText = subtotalElement.textContent.replace('Subtotal: $', '').replace(' COP', '');
        const subtotalNumero = parseFloat(subtotalText.replace(/\./g, '').replace(',', '.'));
        subtotalElement.textContent = `Subtotal: $${formatearNumero(subtotalNumero)} COP`;
    });

    // Formatear el precio unitario
    document.querySelectorAll('.item-carrito').forEach(item => {
        const precioUnitarioElement = item.querySelector('.precio-unitario');
        if (precioUnitarioElement) {
            const precioUnitarioText = precioUnitarioElement.textContent.replace('Precio unitario: $', '').replace(' COP', '');
            const precioUnitarioNumero = parseFloat(precioUnitarioText.replace(/\./g, '').replace(',', '.'));
            precioUnitarioElement.textContent = `Precio unitario: $${formatearNumero(precioUnitarioNumero)} COP`;
        }
    });

    const totalCarritoElement = document.querySelector('.total-carrito h3');
    if (totalCarritoElement) {
        const totalText = totalCarritoElement.textContent.replace('Total: $', '').replace(' COP', '');
        const totalNumero = parseFloat(totalText.replace(/\./g, '').replace(',', '.'));
        totalCarritoElement.textContent = `Total: $${formatearNumero(totalNumero)} COP`;
    }

    // Función para actualizar el total del carrito
    function actualizarTotalCarrito() {
        const items = document.querySelectorAll('.item-carrito');
        let total = 0;

        items.forEach(item => {
            const subtotalElement = item.querySelector('.subtotal');
            if (subtotalElement) {
                const subtotalText = subtotalElement.textContent.replace('Subtotal: $', '').replace(' COP', '');
                const subtotal = parseFloat(subtotalText.replace(/\./g, '').replace(',', '.'));
                total += subtotal;
            }
        });

        const totalCarritoElement = document.querySelector('.total-carrito h3');
        if (totalCarritoElement) {
            totalCarritoElement.textContent = `Total: $${formatearNumero(total)} COP`;
        }
    }

    // Manejar botones de cantidad
    document.querySelectorAll('.btn-cantidad').forEach(btn => {
        btn.addEventListener('click', async function() {
            const itemId = this.dataset.itemId;
            const cantidadElement = this.closest('.cantidad-control').querySelector('.cantidad');
            const cantidad = parseInt(cantidadElement.textContent);
            const nuevaCantidad = this.classList.contains('increase') ? cantidad + 1 : cantidad - 1;

            if (nuevaCantidad > 0) {
                try {
                    const response = await fetch(`/carrito/actualizar/${itemId}/`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                            'X-CSRFToken': csrfToken
                        },
                        body: `cantidad=${nuevaCantidad}`
                    });

                    const data = await response.json();
                    if (data.success) {
                        // Actualizar la cantidad en la interfaz
                        cantidadElement.textContent = nuevaCantidad;

                        // Actualizar el subtotal
                        const subtotalElement = cantidadElement.closest('.item-carrito').querySelector('.subtotal');
                        if (subtotalElement) {
                            subtotalElement.textContent = `Subtotal: $${formatearNumero(data.nuevo_subtotal)} COP`;
                        }

                        // Actualizar el total del carrito
                        actualizarTotalCarrito();
                    } else {
                        alert(data.message || 'Error al actualizar cantidad');
                    }
                } catch (error) {
                    console.error('Error:', error);
                    alert('Error al actualizar cantidad');
                }
            }
        });
    });

    // Manejar eliminación de items
    document.querySelectorAll('.btn-eliminar').forEach(btn => {
        btn.addEventListener('click', async function() {
            if (confirm('¿Está seguro de eliminar este producto del carrito?')) {
                const itemId = this.dataset.itemId;
                try {
                    const response = await fetch(`/carrito/eliminar/${itemId}/`, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': csrfToken
                        }
                    });

                    const data = await response.json();
                    if (data.success) {
                        // Eliminar el ítem del DOM
                        const itemElement = this.closest('.item-carrito');
                        if (itemElement) {
                            itemElement.remove();
                        }

                        // Actualizar el total del carrito
                        actualizarTotalCarrito();
                    } else {
                        alert(data.message);
                    }
                } catch (error) {
                    console.error('Error:', error);
                    alert('Error al eliminar el item');
                }
            }
        });
    });

    // Manejar pago
    const btnPagar = document.getElementById('btn-pagar');
    if (btnPagar) {
        btnPagar.addEventListener('click', function() {
            document.getElementById('modal-nequi').style.display = 'block';
        });
    }

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
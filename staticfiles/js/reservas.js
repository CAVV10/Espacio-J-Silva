document.addEventListener('DOMContentLoaded', function () {
    const servicioSelect = document.getElementById('servicio');
    const desinfeccionFields = document.getElementById('desinfeccion-fields');
    const controlApicolaFields = document.getElementById('control-apicola-fields');
    const jardineriaFields = document.getElementById('jardineria-fields');
    const capacitacionFields = document.getElementById('capacitacion-fields');
    const datosContacto = document.querySelector('.datos-contacto');

    // Oculta todos los campos específicos de servicio
    function ocultarTodosLosCampos() {
        desinfeccionFields.style.display = 'none';
        controlApicolaFields.style.display = 'none';
        jardineriaFields.style.display = 'none';
        capacitacionFields.style.display = 'none';
        datosContacto.style.display = 'none'; // Ocultar datos de contacto inicialmente
    }

    // Muestra los campos según el servicio seleccionado
    servicioSelect.addEventListener('change', function () {
        ocultarTodosLosCampos();

        const servicioSeleccionado = servicioSelect.value;

        if (servicioSeleccionado === '1') {
            desinfeccionFields.style.display = 'block';
            datosContacto.style.display = 'block';
        } else if (servicioSeleccionado === '2') {
            controlApicolaFields.style.display = 'block';
            datosContacto.style.display = 'block';
        } else if (servicioSeleccionado === '3') {
            jardineriaFields.style.display = 'block';
            datosContacto.style.display = 'block';
        } else if (servicioSeleccionado === '4') {
            capacitacionFields.style.display = 'block';
            datosContacto.style.display = 'block';
        }
    });

    // Resto del código de manejo del formulario (sin cambios)
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();

            const fecha = document.getElementById('fecha').value;
            const hora = document.getElementById('hora').value;

            if (!fecha || !hora) {
                mostrarNotificacion('Por favor, complete ambos campos de fecha y hora.', 'error');
                return;
            }

            const fechaHora = `${fecha}T${hora}:00`;
            const fechaHoraInput = document.createElement('input');
            fechaHoraInput.type = 'hidden';
            fechaHoraInput.name = 'fecha_hora';
            fechaHoraInput.value = fechaHora;
            this.appendChild(fechaHoraInput);

            const formData = new FormData(this);

            fetch(this.action, {
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
                    mostrarNotificacion(data.message, 'exito');
                    form.reset();
                    ocultarTodosLosCampos();
                } else {
                    if (data.errors) {
                        for (const field in data.errors) {
                            mostrarNotificacion(data.errors[field], 'error');
                        }
                    } else {
                        mostrarNotificacion(data.message, 'error');
                    }
                }
            })
            .catch(() => {
                mostrarNotificacion('Hubo un error al enviar el formulario.', 'error');
            });
        });
    }
});

// CARRITO DE COMPRAS
// Abrir modales
document.querySelectorAll('.btn-comprar').forEach(btn => {
    btn.addEventListener('click', () => {
        const tipo = btn.closest('.producto').dataset.tipo;
        document.getElementById(`modal-${tipo}`).style.display = 'flex';
    });
});

// Cerrar modales
document.querySelectorAll('.close').forEach(close => {
    close.addEventListener('click', () => {
        close.closest('.modal').style.display = 'none';
    });
});

// Agregar al carrito
document.getElementById('form-extintor').addEventListener('submit', (e) => {
    e.preventDefault();
    agregarAlCarrito('extintor');
});

document.getElementById('form-plano-3d').addEventListener('submit', (e) => {
    e.preventDefault();
    agregarAlCarrito('plano-3d');
});

function agregarAlCarrito(tipo) {
    const form = document.getElementById(`form-${tipo}`);
    const producto = {
        nombre: tipo === 'extintor' ? 'Extintor' : 'Plano 3D',
        precio: calcularPrecio(tipo, form), // Calcula el precio según las opciones
        cantidad: form.querySelector('input[type="number"]').value,
        opciones: Array.from(form.elements).reduce((acc, el) => {
            if (el.name) acc[el.name] = el.value;
            return acc;
        }, {}),
    };

    const carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    carrito.push(producto);
    localStorage.setItem('carrito', JSON.stringify(carrito));
    actualizarCarrito();
    form.reset();
    document.getElementById(`modal-${tipo}`).style.display = 'none';
}

// Función para calcular el precio según las opciones
function calcularPrecio(tipo, form) {
    if (tipo === 'extintor') {
        const opcion = form.querySelector('input[name="opcion-extintor"]:checked').value;
        const tipoExtintor = form.querySelector('select[name="tipo-extintor"]').value;

        // Precios base
        let precio = 0;
        if (tipoExtintor === 'polvo-quimico') precio = 80000;
        else if (tipoExtintor === 'co2') precio = 100000;
        else if (tipoExtintor === 'agua') precio = 120000;

        // Descuento por mantenimiento
        if (opcion === 'mantenimiento') precio -= 50000;

        return precio;
    } else if (tipo === 'plano-3d') {
        const tipoPlano = form.querySelector('select[name="tipo-plano"]').value;
        const escala = form.querySelector('select[name="escala-plano"]').value;

        // Precios base
        let precio = 0;
        if (tipoPlano === 'residencial') precio = 150000;
        else if (tipoPlano === 'comercial') precio = 200000;
        else if (tipoPlano === 'industrial') precio = 250000;

        // Ajuste por escala
        if (escala === '1:50') precio += 0;
        else if (escala === '1:100') precio += 50000;
        else if (escala === '1:200') precio += 100000;

        return precio;
    }
    return 0;
}

// Actualizar carrito
function actualizarCarrito() {
    const carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    const lista = document.getElementById('lista-carrito');
    const total = document.getElementById('total-carrito');

    lista.innerHTML = '';
    let totalPrecio = 0;

    carrito.forEach((item, index) => {
        const li = document.createElement('li');
        let detalles = '';
        if (item.nombre === 'Extintor') {
            detalles = `(${item.opciones['opcion-extintor']}, ${item.opciones['tipo-extintor']})`;
        } else if (item.nombre === 'Plano 3D') {
            detalles = `(${item.opciones['tipo-plano']}, ${item.opciones['escala-plano']})`;
        }
        li.innerHTML = `
            ${item.nombre} ${detalles} - ${item.cantidad} x $${item.precio}
            <button class="btn-aumentar" data-index="${index}">➕</button>
            <button class="btn-disminuir" data-index="${index}">➖</button>
            <button class="btn-eliminar" data-index="${index}">🗑️</button>
        `;
        lista.appendChild(li);
        totalPrecio += item.precio * item.cantidad;
    });

    total.textContent = `$${totalPrecio}`;

    // Agregar eventos a los botones de aumentar, disminuir y eliminar
    document.querySelectorAll('.btn-aumentar').forEach(btn => {
        btn.addEventListener('click', () => {
            const index = btn.getAttribute('data-index');
            aumentarCantidad(index);
        });
    });

    document.querySelectorAll('.btn-disminuir').forEach(btn => {
        btn.addEventListener('click', () => {
            const index = btn.getAttribute('data-index');
            disminuirCantidad(index);
        });
    });

    document.querySelectorAll('.btn-eliminar').forEach(btn => {
        btn.addEventListener('click', () => {
            const index = btn.getAttribute('data-index');
            eliminarProducto(index);
        });
    });
}

// Aumentar cantidad de un producto
function aumentarCantidad(index) {
    const carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    carrito[index].cantidad++;
    localStorage.setItem('carrito', JSON.stringify(carrito));
    actualizarCarrito();
}

// Disminuir cantidad de un producto
function disminuirCantidad(index) {
    const carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    if (carrito[index].cantidad > 1) {
        carrito[index].cantidad--;
    } else {
        eliminarProducto(index); // Si la cantidad es 1, elimina el producto
    }
    localStorage.setItem('carrito', JSON.stringify(carrito));
    actualizarCarrito();
}

// Eliminar un producto del carrito
function eliminarProducto(index) {
    const carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    carrito.splice(index, 1); // Elimina el producto en la posición `index`
    localStorage.setItem('carrito', JSON.stringify(carrito));
    actualizarCarrito();
}

// Mostrar modal de Nequi
document.getElementById('btn-pagar').addEventListener('click', () => {
    const carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    if (carrito.length === 0) {
        alert('Tu carrito está vacío.');
        return;
    }

    const totalPrecio = carrito.reduce((total, item) => total + item.precio * item.cantidad, 0);
    document.getElementById('total-pagar').textContent = `$${totalPrecio}`;
    document.getElementById('monto-pagar').textContent = `$${totalPrecio}`;
    document.getElementById('modal-nequi').style.display = 'flex';
});

// Confirmar pago
document.getElementById('btn-confirmar-pago').addEventListener('click', () => {
    alert('Gracias por tu pago. Tu reserva ha sido confirmada.');
    localStorage.removeItem('carrito'); // Vaciar el carrito
    actualizarCarrito(); // Actualizar la vista del carrito
    document.getElementById('modal-nequi').style.display = 'none';
});

// Inicializar carrito
document.addEventListener('DOMContentLoaded', () => {
    actualizarCarrito();
});
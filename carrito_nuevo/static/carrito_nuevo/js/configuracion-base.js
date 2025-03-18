// Funciones para CSRF token en AJAX requests
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Configurar AJAX para incluir el token CSRF en todas las solicitudes
$(document).ready(function() {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

    // Toggle del menú móvil
    $('.toggle__menu').click(function() {
        $('.nav__list').addClass('show__menu');
    });

    $('.close__menu').click(function() {
        $('.nav__list').removeClass('show__menu');
    });

    // Manejar dropdowns
    $('.dropdown').each(function() {
        const dropdown = $(this);
        const link = dropdown.find('.dropdown__link');
        
        link.click(function(e) {
            e.preventDefault();
            dropdown.toggleClass('active');
            
            // Cerrar otros dropdowns abiertos
            $('.dropdown').not(dropdown).removeClass('active');
        });
    });
});

// Función para mostrar alertas
function showAlert(message, type) {
    const alertDiv = $('<div>').addClass('fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg');
    
    if (type === 'success') {
        alertDiv.addClass('bg-green-100 border border-green-500 text-green-700');
    } else if (type === 'error') {
        alertDiv.addClass('bg-red-100 border border-red-500 text-red-700');
    } else {
        alertDiv.addClass('bg-blue-100 border border-blue-500 text-blue-700');
    }
    
    alertDiv.text(message);
    $('body').append(alertDiv);
    
    // Ocultar después de 3 segundos
    setTimeout(function() {
        alertDiv.fadeOut(300, function() {
            $(this).remove();
        });
    }, 3000);
}

// Función para animar el carrito cuando se añade un producto
function animateCart() {
    const cartIcon = $('.fa-shopping-cart');
    cartIcon.removeClass('animate-bounce-on-add');
    
    // Trigger reflow
    void cartIcon[0].offsetWidth;
    
    cartIcon.addClass('animate-bounce-on-add');
}

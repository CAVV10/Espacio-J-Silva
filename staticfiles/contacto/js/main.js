const navMenu = document.getElementById('nav-menu'),
      toggleMenu = document.getElementById('toggle-menu'),
      closeMenu = document.getElementById('close-menu'),
      dropdowns = document.querySelectorAll('.dropdown');

// Abre y cierra el menú principal
toggleMenu.addEventListener('click', () => {
    navMenu.classList.toggle('show__menu');
});

closeMenu.addEventListener('click', () => {
    navMenu.classList.remove('show__menu');
});

// Lógica para abrir y cerrar los submenús
dropdowns.forEach(dropdown => {
    const link = dropdown.querySelector('.dropdown__link');
    
    link.addEventListener('click', (e) => {
        e.preventDefault(); // Evita el comportamiento predeterminado del enlace
        dropdown.classList.toggle('active');
        
        // Opcional: Cierra otros submenús abiertos
        dropdowns.forEach(otherDropdown => {
            if (otherDropdown !== dropdown) {
                otherDropdown.classList.remove('active');
            }
        });
    });
});

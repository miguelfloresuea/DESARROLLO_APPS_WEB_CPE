/* =======================================================
   ARCHIVO: validaciones.js
   Responsable: Jessica
   Función: Validar el campo Nombre en tiempo real
======================================================= */

const campoNombre = document.getElementById('sol-nombre');

// Solo permite letras y espacios mientras escribe
campoNombre.addEventListener('keypress', function (e) {
    const soloLetras = /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]$/;
    if (!soloLetras.test(e.key)) e.preventDefault();
});

// Valida que el nombre no esté vacío y tenga mínimo 3 caracteres
function validarNombre() {
    const valor = campoNombre.value.trim();
    const error = document.getElementById('error-nombre');

    if (valor === '') {
        error.textContent = '⚠ Escribe tu nombre.';
        error.style.display = 'block';
        campoNombre.classList.add('is-invalid');
        campoNombre.classList.remove('is-valid');
        return false;
    }
    if (valor.length < 3) {
        error.textContent = ' Mínimo 3 caracteres.';
        error.style.display = 'block';
        campoNombre.classList.add('is-invalid');
        campoNombre.classList.remove('is-valid');
        return false;
    }
    error.style.display = 'none';
    campoNombre.classList.remove('is-invalid');
    campoNombre.classList.add('is-valid');
    return true;
}

// Escucha mientras escribe y cuando sale del campo
campoNombre.addEventListener('input', validarNombre);
campoNombre.addEventListener('blur', validarNombre);
// Transforma el nombre: primera letra de cada palabra en mayúscula
// (equivalente al filtro |upper visto en la guía de plantillas, aplicado por palabra)
function capitalizarNombre(nombre) {
    return nombre
        .split(' ')
        .filter(palabra => palabra.length > 0)
        .map(palabra => palabra.charAt(0).toUpperCase() + palabra.slice(1).toLowerCase())
        .join(' ');
}
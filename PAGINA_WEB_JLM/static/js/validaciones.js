/* =======================================================
   ARCHIVO: validaciones.js
   Responsable: Jessica
   Función: Validar el campo Nombre en tiempo real
   ACTUALIZADO Semana 8:
   - Alerta Bootstrap dinámica en vez de solo texto plano
   - Spinner Bootstrap que simula verificación del campo
======================================================= */

const campoNombre = document.getElementById('sol-nombre');
const spinnerNombre = document.getElementById('spinner-nombre');

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
        mostrarErrorNombre('⚠ Escribe tu nombre.');
        return false;
    }
    if (valor.length < 3) {
        mostrarErrorNombre('⚠ Mínimo 3 caracteres.');
        return false;
    }

    error.style.display = 'none';
    error.classList.remove('alert', 'alert-danger', 'small', 'mt-1');
    campoNombre.classList.remove('is-invalid');
    campoNombre.classList.add('is-valid');
    return true;
}

// Muestra el error como alerta Bootstrap (en vez de texto plano)
function mostrarErrorNombre(mensaje) {
    const error = document.getElementById('error-nombre');
    error.textContent = mensaje;
    error.className = 'alert alert-danger py-1 px-2 mt-1 small';
    error.style.display = 'block';
    campoNombre.classList.add('is-invalid');
    campoNombre.classList.remove('is-valid');
}

// Simula verificación del campo mostrando un spinner Bootstrap breve
function mostrarSpinnerNombre() {
    if (!spinnerNombre) return;
    spinnerNombre.style.display = 'block';
    setTimeout(() => {
        spinnerNombre.style.display = 'none';
    }, 500);
}

// Escucha mientras escribe y cuando sale del campo
campoNombre.addEventListener('input', validarNombre);
campoNombre.addEventListener('blur', function () {
    mostrarSpinnerNombre();
    validarNombre();
});

// Transforma el nombre: primera letra de cada palabra en mayúscula
function capitalizarNombre(nombre) {
    return nombre
        .split(' ')
        .filter(palabra => palabra.length > 0)
        .map(palabra => palabra.charAt(0).toUpperCase() + palabra.slice(1).toLowerCase())
        .join(' ');
}
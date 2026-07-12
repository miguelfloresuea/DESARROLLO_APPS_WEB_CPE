/* =======================================================
   ARCHIVO: formulario.js
   Responsable: Lisseth 
   Función: Validar Descripción y Categoría
======================================================= */

const campoDescripcion = document.getElementById('sol-descripcion');
const campoCategoria = document.getElementById('sol-categoria');

// Valida que la descripción no esté vacía y tenga mínimo 10 caracteres
function validarDescripcion() {
    const valor = campoDescripcion.value.trim();
    const error = document.getElementById('error-descripcion');

    if (valor === '') {
        error.textContent = '⚠️ Escribe una descripción.';
        error.style.display = 'block';
        campoDescripcion.classList.add('is-invalid');
        campoDescripcion.classList.remove('is-valid');
        return false;
    }
    if (valor.length < 10) {
        error.textContent = '⚠️ Mínimo 10 caracteres.';
        error.style.display = 'block';
        campoDescripcion.classList.add('is-invalid');
        campoDescripcion.classList.remove('is-valid');
        return false;
    }
    error.style.display = 'none';
    campoDescripcion.classList.remove('is-invalid');
    campoDescripcion.classList.add('is-valid');
    return true;
}

// Valida que se haya elegido una categoría
function validarCategoria() {
    const error = document.getElementById('error-categoria');

    if (campoCategoria.value === '') {
        error.style.display = 'block';
        campoCategoria.classList.add('is-invalid');
        campoCategoria.classList.remove('is-valid');
        return false;
    }
    error.style.display = 'none';
    campoCategoria.classList.remove('is-invalid');
    campoCategoria.classList.add('is-valid');
    return true;
}

// Validación en tiempo real
campoDescripcion.addEventListener('input', validarDescripcion);
campoDescripcion.addEventListener('blur', validarDescripcion);
campoCategoria.addEventListener('change', validarCategoria);
campoCategoria.addEventListener('blur', validarCategoria);

// Condicional según el estado de los datos: muestra u oculta
// el mensaje "Aún no hay solicitudes" dependiendo del arreglo
// "solicitudes" definido en registro.js
function actualizarMensajeEstado() {
    const mensaje = document.getElementById('mensaje-vacio');
    if (!mensaje) return;
    mensaje.style.display = solicitudes.length === 0 ? 'block' : 'none';
}
/* =======================================================
   ARCHIVO: registro.js
   Responsable: Miguel
   Función: Envío, vista previa, registro con arreglo,
   renderizado dinámico, conteo y eliminación
   ------------------------------------------------------
   ACTUALIZADO Semana 7:
   - Las solicitudes ahora se guardan en un arreglo de
     objetos (antes se creaban directo en el DOM).
   - renderizarSolicitudes() recorre el arreglo con
     forEach y regenera la lista completa.
   - Usa capitalizarNombre() de validaciones.js.
   - Llama a actualizarMensajeEstado() de formulario.js.
======================================================= */

const formulario = document.getElementById('formulario-solicitud');
const listaSolicitudes = document.getElementById('lista-solicitudes');
const contadorRegistros = document.getElementById('contador-registros');

// Arreglo de objetos: cada solicitud = {nombre, descripcion, categoria}
let solicitudes = [];

// Convierte texto en HTML seguro (evita inyección de código)
function escapeHTML(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

// Escucha el envío del formulario
formulario.addEventListener('submit', function (evento) {
    evento.preventDefault();

    const ok = validarNombre() && validarDescripcion() && validarCategoria();
    if (!ok) return;

    const nombre = document.getElementById('sol-nombre').value.trim();
    const descripcion = document.getElementById('sol-descripcion').value.trim();
    const categoria = document.getElementById('sol-categoria').value;

    mostrarVistaPrevia(nombre, descripcion, categoria);
});

// Muestra la vista previa antes de confirmar el envío
function mostrarVistaPrevia(nombre, descripcion, categoria) {
    const previaAnterior = document.getElementById('vista-previa');
    if (previaAnterior) previaAnterior.remove();

    const previa = document.createElement('div');
    previa.id = 'vista-previa';
    previa.classList.add('alert', 'alert-info', 'mt-3', 'col-12');
    previa.innerHTML = `
        <h5 class="mb-3">📋 Revisa tu solicitud:</h5>
        <p class="mb-1"><strong>Nombres y Apellidos:</strong> ${escapeHTML(nombre)}</p>
        <p class="mb-1"><strong>Categoría:</strong> ${escapeHTML(categoria)}</p>
        <p class="mb-3"><strong>Mensaje:</strong> ${escapeHTML(descripcion)}</p>
        <div class="d-flex gap-2">
            <button type="button" id="btn-editar" class="btn btn-secondary">✏️ Editar</button>
            <button type="button" id="btn-enviar" class="btn btn-success">📨 Enviar Solicitud</button>
        </div>
    `;
    formulario.appendChild(previa);

    document.getElementById('btn-editar').addEventListener('click', () => previa.remove());

    document.getElementById('btn-enviar').addEventListener('click', function () {
        previa.remove();
        registrarSolicitud(nombre, descripcion, categoria);
    });
}

// Agrega la solicitud al arreglo y actualiza la vista
function registrarSolicitud(nombre, descripcion, categoria) {
    const nombreFormateado = capitalizarNombre(nombre); // función de Jessica (validaciones.js)

    solicitudes.push({
        nombre: nombreFormateado,
        descripcion: descripcion,
        categoria: categoria
    });

    renderizarSolicitudes();

    // Mensaje de éxito
    const alerta = document.createElement('div');
    alerta.classList.add('alert', 'alert-success', 'mt-2', 'col-12');
    alerta.textContent = '✅ Su solicitud fue enviada con éxito.';
    formulario.appendChild(alerta);
    setTimeout(() => alerta.remove(), 3000);

    // Limpia el formulario y los estilos de validación
    formulario.reset();
    [campoNombre, campoDescripcion, campoCategoria].forEach(campo => {
        campo.classList.remove('is-valid', 'is-invalid');
    });
}

// Recorre el arreglo "solicitudes" y regenera la lista en pantalla
// (Estructura repetitiva pedida en la Semana 7, equivalente a un {% for %} de plantillas)
function renderizarSolicitudes() {
    listaSolicitudes.innerHTML = '';

    solicitudes.forEach((solicitud, indice) => {
        const item = document.createElement('div');
        item.classList.add('list-group-item', 'd-flex', 'justify-content-between', 'align-items-start', 'mb-2', 'rounded', 'shadow-sm');
        item.innerHTML = `
            <div>
                <p class="mb-1"><strong>Nombres y Apellidos:</strong> ${escapeHTML(solicitud.nombre)}</p>
                <p class="mb-1"><strong>Categoría:</strong> ${escapeHTML(solicitud.categoria)}</p>
                <p class="mb-0 text-muted">Mensaje: ${escapeHTML(solicitud.descripcion)}</p>
            </div>
            <button type="button" class="btn btn-danger btn-sm ms-3">🗑 Eliminar</button>
        `;

        item.querySelector('button').addEventListener('click', function () {
            eliminarSolicitud(indice);
        });

        listaSolicitudes.appendChild(item);
    });

    contadorRegistros.textContent = solicitudes.length;

    // Condicional según el estado de los datos (función de Lisseth, formulario.js)
    if (typeof actualizarMensajeEstado === 'function') {
        actualizarMensajeEstado();
    }
}

// Elimina una solicitud del arreglo según su posición
function eliminarSolicitud(indice) {
    solicitudes.splice(indice, 1);
    renderizarSolicitudes();
}
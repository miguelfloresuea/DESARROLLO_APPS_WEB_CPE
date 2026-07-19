/* =======================================================
   ARCHIVO: registro.js
   Responsable: Miguel
   Función: Envío, vista previa, registro con arreglo,
   renderizado dinámico en TABLA, conteo, modal y eliminación
   ------------------------------------------------------
   ACTUALIZADO Semana 8:
   - La lista ahora se renderiza como tabla Bootstrap
   - Botón "Ver" abre un modal Bootstrap con el detalle
======================================================= */

const formulario = document.getElementById('formulario-solicitud');
// CORREGIDO: Vinculado al elemento ID tbody real del HTML ('tabla-solicitudes')
const listaSolicitudes = document.getElementById('tabla-solicitudes');
const contadorRegistros = document.getElementById('contador-registros');

// Arreglo de objetos: cada solicitud = {nombre, descripcion, categoria}
let solicitudes = [];

// Convierte texto en HTML seguro (evita inyección de código XSS)
function escapeHTML(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

// CORREGIDO: Mudado de forma nativa a este script para evitar ReferenceError de archivos cruzados
function actualizarMensajeEstado() {
    const mensaje = document.getElementById('mensaje-vacio');
    if (!mensaje) return;
    mensaje.style.display = solicitudes.length === 0 ? 'block' : 'none';
}

// Escucha el envío del formulario
formulario.addEventListener('submit', function (evento) {
    evento.preventDefault();

    // Verificación segura ante cargas asíncronas
    const ok = (typeof validarNombre === 'function' ? validarNombre() : true) && 
               (typeof validarDescripcion === 'function' ? validarDescripcion() : true) && 
               (typeof validarCategoria === 'function' ? validarCategoria() : true);
               
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
    const nombreFormateado = typeof capitalizarNombre === 'function' ? capitalizarNombre(nombre) : nombre;

    solicitudes.push({
        nombre: nombreFormateado,
        descripcion: descripcion,
        categoria: categoria
    });

    renderizarSolicitudes();

    const alerta = document.createElement('div');
    alerta.classList.add('alert', 'alert-success', 'mt-2', 'col-12');
    alerta.textContent = '✅ Su solicitud fue enviada con éxito.';
    formulario.appendChild(alerta);
    setTimeout(() => alerta.remove(), 3000);

    formulario.reset();
    
    // CORREGIDO: Busca los campos reactivos de forma local en el formulario para limpiar los bordes verdes/rojos de Bootstrap
    formulario.querySelectorAll('.form-control, .form-select').forEach(campo => {
        campo.classList.remove('is-valid', 'is-invalid');
    });

    if (typeof actualizarContadorDescripcion === 'function') {
        actualizarContadorDescripcion();
    }
}

// Recorre el arreglo "solicitudes" y regenera la TABLA en pantalla
function renderizarSolicitudes() {
    if (!listaSolicitudes) return;
    listaSolicitudes.innerHTML = '';

    solicitudes.forEach((solicitud, indice) => {
        const fila = document.createElement('tr');
        fila.innerHTML = `
            <td>${escapeHTML(solicitud.nombre)}</td>
            <td><span class="badge bg-info text-dark">${escapeHTML(solicitud.categoria)}</span></td>
            <td>${escapeHTML(solicitud.descripcion.substring(0, 20))}${solicitud.descripcion.length > 20 ? '...' : ''}</td>
            <td>
                <button type="button" class="btn btn-primary btn-sm ver-detalle">👁 Ver</button>
                <button type="button" class="btn btn-danger btn-sm eliminar">🗑</button>
            </td>
        `;

        fila.querySelector('.ver-detalle').addEventListener('click', function () {
            mostrarDetalleModal(solicitud);
        });

        fila.querySelector('.eliminar').addEventListener('click', function () {
            eliminarSolicitud(indice);
        });

        listaSolicitudes.appendChild(fila);
    });

    if (contadorRegistros) {
        contadorRegistros.textContent = solicitudes.length;
    }

    actualizarMensajeEstado();
}

// Llena y abre el modal Bootstrap con el detalle de una solicitud
function mostrarDetalleModal(solicitud) {
    document.getElementById('modal-nombre').textContent = solicitud.nombre;
    document.getElementById('modal-categoria').textContent = solicitud.categoria;
    document.getElementById('modal-descripcion').textContent = solicitud.descripcion;

    const modal = new bootstrap.Modal(document.getElementById('modalDetalle'));
    modal.show();
}

// Elimina una solicitud del arreglo según su posición
function eliminarSolicitud(indice) {
    solicitudes.splice(indice, 1);
    renderizarSolicitudes();
}
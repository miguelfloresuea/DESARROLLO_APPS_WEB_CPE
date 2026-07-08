/* =======================================================
   ARCHIVO: registro.js
   Responsable: Miguel
   Función: Envío, vista previa, registro, conteo y eliminación
   ------------------------------------------------------
   CORREGIDO:
   - Botones de la vista previa ahora usan type="button"
     (antes disparaban un submit extra del formulario).
   - Se agrega escapeHTML() para evitar inyección de HTML
     en los campos nombre y descripción.
   - previa y alerta usan class="col-12" para alinearse
     bien dentro del <form class="row g-3">.
======================================================= */

const formulario = document.getElementById('formulario-solicitud');
const listaSolicitudes = document.getElementById('lista-solicitudes');
const contadorRegistros = document.getElementById('contador-registros');
let totalRegistros = 0;

// Convierte texto en HTML seguro (evita que <script> o etiquetas
// escritas por el usuario se interpreten como código/HTML real)
function escapeHTML(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

// Escucha el envío del formulario
formulario.addEventListener('submit', function (evento) {
    evento.preventDefault(); // evita que la página se recargue

    // Usa las funciones de validaciones.js y formulario.js
    const ok = validarNombre() && validarDescripcion() && validarCategoria();
    if (!ok) return; // si hay error, no continúa

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

    // Botón Editar: cierra la vista previa para corregir datos
    document.getElementById('btn-editar').addEventListener('click', () => previa.remove());

    // Botón Enviar: confirma y registra
    document.getElementById('btn-enviar').addEventListener('click', function () {
        previa.remove();
        registrarSolicitud(nombre, descripcion, categoria);
    });
}

// Crea el registro visual, muestra alerta y permite eliminar
function registrarSolicitud(nombre, descripcion, categoria) {

    // Mensaje de éxito
    const alerta = document.createElement('div');
    alerta.classList.add('alert', 'alert-success', 'mt-2', 'col-12');
    alerta.textContent = '✅ Su solicitud fue enviada con éxito.';
    formulario.appendChild(alerta);
    setTimeout(() => alerta.remove(), 3000);

    // Nuevo registro en la lista
    const nuevoItem = document.createElement('div');
    nuevoItem.classList.add('list-group-item', 'd-flex', 'justify-content-between', 'align-items-start', 'mb-2', 'rounded', 'shadow-sm');
    nuevoItem.innerHTML = `
        <div>
            <p class="mb-1"><strong>Nombres y Apellidos:</strong> ${escapeHTML(nombre)}</p>
            <p class="mb-1"><strong>Categoría:</strong> ${escapeHTML(categoria)}</p>
            <p class="mb-0 text-muted">Mensaje: ${escapeHTML(descripcion)}</p>
        </div>
        <button type="button" class="btn btn-danger btn-sm ms-3">🗑 Eliminar</button>
    `;

    // Botón eliminar
    nuevoItem.querySelector('button').addEventListener('click', function () {
        nuevoItem.remove();
        totalRegistros--;
        contadorRegistros.textContent = totalRegistros;
    });

    listaSolicitudes.appendChild(nuevoItem);
    totalRegistros++;
    contadorRegistros.textContent = totalRegistros;

    // Limpia el formulario y los estilos de validación
    formulario.reset();
    [campoNombre, campoDescripcion, campoCategoria].forEach(campo => {
        campo.classList.remove('is-valid', 'is-invalid');
    });
}
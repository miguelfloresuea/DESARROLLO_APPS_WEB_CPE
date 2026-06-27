// PARTE 1: JESSICA PESANTEZ

const formulario = document.getElementById('formulario-solicitud');
const listaSolicitudes = document.getElementById('lista-solicitudes');
const contadorRegistros = document.getElementById('contador-registros');
let totalRegistros = 0;

formulario.addEventListener('submit', function(evento) {
    evento.preventDefault();

    const nombre      = document.getElementById('sol-nombre').value.trim();
    const descripcion = document.getElementById('sol-descripcion').value.trim();
    const categoria   = document.getElementById('sol-categoria').value;

    // Ocultar errores anteriores
    document.getElementById('error-nombre').style.display      = 'none';
    document.getElementById('error-descripcion').style.display = 'none';
    document.getElementById('error-categoria').style.display   = 'none';

    // Validar campos vacíos
    let hayError = false;
    if (nombre === '')      { document.getElementById('error-nombre').style.display = 'block'; hayError = true; }
    if (descripcion === '') { document.getElementById('error-descripcion').style.display = 'block'; hayError = true; }
    if (categoria === '')   { document.getElementById('error-categoria').style.display = 'block'; hayError = true; }
    if (hayError) return;

    // Crear elemento del registro
    const nuevoItem = document.createElement('div');
    nuevoItem.classList.add('list-group-item', 'd-flex', 'justify-content-between', 'align-items-start', 'mb-2', 'rounded', 'shadow-sm');

    nuevoItem.innerHTML = `
        <div>
            <strong class="text-primary">${nombre}</strong>
            <p class="mb-1 text-muted">${descripcion}</p>
            <span class="badge bg-secondary">${categoria}</span>
        </div>
        <button class="btn btn-danger btn-sm ms-3">🗑 Eliminar</button>
    `;

    // Botón eliminar
    nuevoItem.querySelector('button').addEventListener('click', function() {
        nuevoItem.remove();
        totalRegistros--;
        contadorRegistros.textContent = totalRegistros;
    });

    listaSolicitudes.appendChild(nuevoItem);
    totalRegistros++;
    contadorRegistros.textContent = totalRegistros;
    formulario.reset();
});
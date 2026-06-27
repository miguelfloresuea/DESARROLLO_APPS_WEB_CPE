// Seleccionar elementos del HTML
const formulario = document.getElementById('formulario-solicitud');
const listaSolicitudes = document.getElementById('lista-solicitudes');
const contadorRegistros = document.getElementById('contador-registros');
let totalRegistros = 0;

// Solo permitir letras y espacios en Nombres y Apellidos
document.getElementById('sol-nombre').addEventListener('keypress', function(e) {
    const soloLetras = /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]$/;
    if (!soloLetras.test(e.key)) e.preventDefault();
});

// Escuchar el evento submit del formulario
formulario.addEventListener('submit', function(evento) {
    evento.preventDefault();

    // Obtener los valores de los campos
    const nombre      = document.getElementById('sol-nombre').value.trim();
    const descripcion = document.getElementById('sol-descripcion').value.trim();
    const categoria   = document.getElementById('sol-categoria').value;

    // Ocultar errores anteriores
    document.getElementById('error-nombre').style.display      = 'none';
    document.getElementById('error-descripcion').style.display = 'none';
    document.getElementById('error-categoria').style.display   = 'none';
    document.getElementById('sol-nombre').classList.remove('is-invalid');
    document.getElementById('sol-descripcion').classList.remove('is-invalid');
    document.getElementById('sol-categoria').classList.remove('is-invalid');

    // Validar campos vacíos
    let hayError = false;
    if (nombre === '') {
        document.getElementById('error-nombre').style.display = 'block';
        document.getElementById('sol-nombre').classList.add('is-invalid');
        hayError = true;
    }
    if (descripcion === '') {
        document.getElementById('error-descripcion').style.display = 'block';
        document.getElementById('sol-descripcion').classList.add('is-invalid');
        hayError = true;
    }
    if (categoria === '') {
        document.getElementById('error-categoria').style.display = 'block';
        document.getElementById('sol-categoria').classList.add('is-invalid');
        hayError = true;
    }
    if (hayError) return;

    // Eliminar vista previa anterior si existe
    const previaAnterior = document.getElementById('vista-previa');
    if (previaAnterior) previaAnterior.remove();

    // Mostrar vista previa para que el usuario revise sus datos
    const previa = document.createElement('div');
    previa.id = 'vista-previa';
    previa.classList.add('alert', 'alert-info', 'mt-3');
    previa.innerHTML = `
        <h5 class="mb-3">📋 Revisa tu solicitud:</h5>
        <p class="mb-1"><strong>Nombres y Apellidos:</strong> ${nombre}</p>
        <p class="mb-1"><strong>Categoría:</strong> ${categoria}</p>
        <p class="mb-3"><strong>Mensaje:</strong> ${descripcion}</p>
        <div class="d-flex gap-2">
            <button id="btn-editar" class="btn btn-secondary">✏️ Editar</button>
            <button id="btn-enviar" class="btn btn-success">📨 Enviar Solicitud</button>
        </div>
    `;
    formulario.appendChild(previa);

    // Botón Editar: cierra la vista previa para corregir datos
    document.getElementById('btn-editar').addEventListener('click', function() {
        previa.remove();
    });

    // Botón Enviar: confirma y guarda el registro
    document.getElementById('btn-enviar').addEventListener('click', function() {
        previa.remove();

        // Mostrar mensaje de éxito
        const alerta = document.createElement('div');
        alerta.classList.add('alert', 'alert-success', 'mt-2');
        alerta.textContent = '✅ Su solicitud fue enviada con éxito.';
        formulario.appendChild(alerta);
        setTimeout(() => alerta.remove(), 3000);

        // Crear el registro en la lista
        const nuevoItem = document.createElement('div');
        nuevoItem.classList.add('list-group-item', 'd-flex', 'justify-content-between', 'align-items-start', 'mb-2', 'rounded', 'shadow-sm');
        nuevoItem.innerHTML = `
            <div>
                <p class="mb-1"><strong>Nombres y Apellidos:</strong> ${nombre}</p>
                <p class="mb-1"><strong>Categoría:</strong> ${categoria}</p>
                <p class="mb-0 text-muted">Mensaje: ${descripcion}</p>
            </div>
            <button class="btn btn-danger btn-sm ms-3">🗑 Eliminar</button>
        `;

        // Botón eliminar registro
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
});
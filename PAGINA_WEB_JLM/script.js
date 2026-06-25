// PARTE 1: DESARROLLADO POR JESSICA PESANTEZ
const formulario = document.getElementById('formulario-contacto');
const listaSolicitudes = document.getElementById('lista-solicitudes');
const contadorRegistros = document.getElementById('contador-registros');
const mensajeValidacion = document.getElementById('mensaje-validacion');

// Variable para llevar el total de registros
let totalRegistros = 0;

// Capturar el evento 'submit' cuando se envía el formulario
formulario.addEventListener('submit', function (evento) {
    // Evitar que la página se recargue sola
    evento.preventDefault();

    // Obtener los valores de los campos del formulario
    const nombre = document.getElementById('nombre').value.trim();
    const email = document.getElementById('email').value.trim();
    const categoria = document.getElementById('categoria').value.trim();
    const mensaje = document.getElementById('mensaje').value.trim();

    // Validar que los campos no estén vacíos
    if (nombre === "" || email === "" || categoria === "" || mensaje === "") {
        mensajeValidacion.innerHTML = `
            <div class="alert alert-danger" role="alert">
                Por favor, llene todos los campos del formulario.
            </div>
        `;
        return; // Detiene el código si faltan datos
    }

    // Mensaje de éxito dinámico
    mensajeValidacion.innerHTML = `
        <div class="alert alert-success" role="alert">
            Solicitud registrada correctamente.
        </div>
    `;

    // PARTE 2: DESARROLLADO POR LISSETH PUCO
    // 1. Crear el elemento contenedor de la solicitud
    const nuevoElemento = document.createElement('div');
    nuevoElemento.classList.add('list-group-item', 'mb-2', 'p-3', 'border', 'rounded', 'd-flex', 'justify-content-between', 'align-items-start');

    // 2. Insertar el texto en la interfaz usando las variables de Jessica
    const contenidoTexto = document.createElement('div');
    contenidoTexto.innerHTML = `
        <strong>Nombre:</strong> ${nombre} <br>
        <strong>Categoría:</strong> ${categoria} <br>
        <small class="text-muted">Mensaje: ${mensaje}</small>
    `;
    nuevoElemento.appendChild(contenidoTexto);

    // PARTE 3: DESARROLLADO POR MIGUEL FLORES
    // 1. Crear botón de eliminar y manejar su evento click
    const botonEliminar = document.createElement('button');
    botonEliminar.textContent = 'Eliminar';
    botonEliminar.classList.add('btn', 'btn-sm', 'btn-outline-danger');

    botonEliminar.addEventListener('click', function () {
        nuevoElemento.remove();
        totalRegistros--;
        contadorRegistros.textContent = totalRegistros;
    });

    nuevoElemento.appendChild(botonEliminar);

    // 2. Agregar la tarjeta al contenedor de la página
    listaSolicitudes.appendChild(nuevoElemento);

    // 3. Sumar 1 al contador de registros global
    totalRegistros++;
    contadorRegistros.textContent = totalRegistros;

    // 4. Limpiar el formulario para nuevos mensajes
    formulario.reset();
});
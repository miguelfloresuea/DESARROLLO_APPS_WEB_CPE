// PARTE 1: DESARROLLADO POR JESSICA PESANTEZ
const formulario = document.getElementById('formulario-contacto');
const listaSolicitudes = document.getElementById('lista-solicitudes');
const contadorRegistros = document.getElementById('contador-registros');
// Variable para llevar el total de registros
let totalRegistros = 0;

// Capturar el evento 'submit' cuando se envía el formulario
formulario.addEventListener('submit', function(evento) {
// Evitar que la página se recargue sola
    evento.preventDefault();

    // Obtener los valores de los campos del formulario
    const nombre = document.getElementById('nombre').value.trim();
    const email = document.getElementById('email').value.trim();
    const asunto = document.getElementById('asunto').value.trim();
    const mensaje = document.getElementById('mensaje').value.trim();
    // Validar que los campos no estén vacíos
    if (nombre === "" || email === "" || asunto === "" || mensaje === "") {
        alert("Por favor, llene todos los campos del formulario.");
        return; // Detiene el código si faltan datos
    }
    });
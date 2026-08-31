from flask import Flask, render_template, request

app = Flask(__name__)

app.config['SECRET_KEY'] = 'jlmconnect360-clave-secreta-2026'

planes = [
    {"nombre": "Plan Residencial", "velocidad": "20 Mbps", "precio": "$18.00", "descripcion": "Ideal para navegación, streaming y videollamadas familiares."},
    {"nombre": "Plan Empresarial", "velocidad": "50 Mbps simétrico", "precio": "$45.00", "descripcion": "Conexión de alta velocidad y estabilidad para negocios."},
    {"nombre": "Plan Educativo", "velocidad": "15 Mbps", "precio": "$12.00", "descripcion": "Tarifa preferencial para instituciones educativas."},
    {"nombre": "Plan Rural", "velocidad": "10 Mbps", "precio": "$15.00", "descripcion": "Cobertura mediante enlaces punto a multipunto de 5 GHz."},
]

clientes = [
    {"id": 1, "nombre": "Carlos Andrade", "sector": "Macas Centro", "plan": "Residencial", "estado": "Activo"},
    {"id": 2, "nombre": "Distribuidora Amazónica", "sector": "Zona Industrial", "plan": "Empresarial", "estado": "Activo"},
    {"id": 3, "nombre": "Unidad Educativa Emanuel", "sector": "Macas Centro", "plan": "Educativo", "estado": "Activo"},
    {"id": 4, "nombre": "Familia Chumpi", "sector": "Sinaí", "plan": "Rural", "estado": "Pendiente instalación"},
]

proveedores = [
    {"id": 1, "nombre": "TP-Link Ecuador", "producto": "Routers y repetidores", "contacto": "ventas@tplink.ec"},
    {"id": 2, "nombre": "Ubiquiti Networks", "producto": "Equipos punto a multipunto 5 GHz", "contacto": "soporte@ubnt.com"},
    {"id": 3, "nombre": "Fibercorp", "producto": "Cable de fibra óptica y accesorios", "contacto": "contacto@fibercorp.ec"},
]

facturas = [
    {"numero": "F001-000123", "cliente": "Carlos Andrade", "monto": "$18.00", "estado": "Pagada"},
    {"numero": "F001-000124", "cliente": "Distribuidora Amazónica", "monto": "$45.00", "estado": "Pendiente"},
    {"numero": "F001-000125", "cliente": "Unidad Educativa Emanuel", "monto": "$12.00", "estado": "Pagada"},
]


@app.route('/')
def inicio():
    return render_template('index.html')


@app.route('/productos')
def productos():
    return render_template('productos.html', planes=planes)


@app.route('/clientes')
def clientes_route():
    return render_template('clientes.html', clientes=clientes)


@app.route('/proveedores')
def proveedores_route():
    return render_template('proveedores.html', proveedores=proveedores)


@app.route('/facturacion')
def facturacion():
    return render_template('facturacion.html', facturas=facturas)


@app.route('/contacto', methods=['POST'])
def procesar_contacto():
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    asunto = request.form.get('asunto')
    mensaje = request.form.get('mensaje')
    return render_template(
        'confirmacion.html',
        nombre=nombre,
        email=email,
        asunto=asunto,
        mensaje=mensaje
    )


if __name__ == '__main__':
    app.run(debug=True)
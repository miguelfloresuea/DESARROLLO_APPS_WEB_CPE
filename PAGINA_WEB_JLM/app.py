from flask import Flask, render_template, request, redirect, url_for
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from database import init_db, get_connection

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jlmconnect360-clave-secreta-2026'

init_db()

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
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos')
    planes_db = cursor.fetchall()
    conn.close()
    return render_template('productos.html', planes=planes_db)


@app.route('/productos/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO productos (nombre, velocidad, precio, descripcion) VALUES (?, ?, ?, ?)',
            (form.nombre.data, form.velocidad.data, form.precio.data, form.descripcion.data)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('productos'))
    return render_template('formulario_producto.html', form=form)


@app.route('/clientes')
def clientes_route():
    return render_template('clientes.html', clientes=clientes)


@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def nuevo_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        nuevo_id = len(clientes) + 1
        clientes.append({
            "id": nuevo_id,
            "nombre": form.nombre.data,
            "sector": form.sector.data,
            "plan": form.plan.data,
            "estado": form.estado.data
        })
        return redirect(url_for('clientes_route'))
    return render_template('formulario_cliente.html', form=form)


@app.route('/proveedores')
def proveedores_route():
    return render_template('proveedores.html', proveedores=proveedores)


@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
def nuevo_proveedor():
    form = ProveedorForm()
    if form.validate_on_submit():
        nuevo_id = len(proveedores) + 1
        proveedores.append({
            "id": nuevo_id,
            "nombre": form.nombre.data,
            "producto": form.producto.data,
            "contacto": form.contacto.data
        })
        return redirect(url_for('proveedores_route'))
    return render_template('formulario_proveedor.html', form=form)


@app.route('/facturacion')
def facturacion():
    return render_template('facturacion.html', facturas=facturas)


@app.route('/facturacion/nueva', methods=['GET', 'POST'])
def nueva_factura():
    form = FacturacionForm()
    if form.validate_on_submit():
        facturas.append({
            "numero": form.numero.data,
            "cliente": form.cliente.data,
            "monto": form.monto.data,
            "estado": form.estado.data
        })
        return redirect(url_for('facturacion'))
    return render_template('formulario_facturacion.html', form=form)


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
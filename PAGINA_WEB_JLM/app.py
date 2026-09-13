from flask import Flask, render_template, request, redirect, url_for
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from conexion.conexion import get_connection
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jlmconnect360-clave-secreta-2026'

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
    cursor.execute('SELECT id_producto, nombre, velocidad, precio, descripcion FROM productos')
    filas = cursor.fetchall()
    cursor.close()
    conn.close()
    planes_db = []
    for fila in filas:
        planes_db.append({
            "id_producto": fila[0],
            "nombre": fila[1],
            "velocidad": fila[2],
            "precio": fila[3],
            "descripcion": fila[4]
        })
    return render_template('productos.html', planes=planes_db)


@app.route('/productos/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO productos (nombre, velocidad, precio, descripcion) VALUES (%s, %s, %s, %s)',
            (form.nombre.data, form.velocidad.data, form.precio.data, form.descripcion.data)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('productos'))
    return render_template('formulario_producto.html', form=form)


@app.route('/productos/editar/<int:id_producto>', methods=['GET', 'POST'])
def editar_producto(id_producto):
    conn = get_connection()
    cursor = conn.cursor()

    form = ProductoForm()
    if form.validate_on_submit():
        cursor.execute(
            'UPDATE productos SET nombre = %s, velocidad = %s, precio = %s, descripcion = %s WHERE id_producto = %s',
            (form.nombre.data, form.velocidad.data, form.precio.data, form.descripcion.data, id_producto)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('productos'))

    if request.method == 'GET':
        cursor.execute('SELECT nombre, velocidad, precio, descripcion FROM productos WHERE id_producto = %s', (id_producto,))
        producto = cursor.fetchone()
        if producto:
            form.nombre.data = producto[0]
            form.velocidad.data = producto[1]
            form.precio.data = producto[2]
            form.descripcion.data = producto[3]

    cursor.close()
    conn.close()
    return render_template('formulario_producto.html', form=form)


@app.route('/productos/eliminar/<int:id_producto>')
def eliminar_producto(id_producto):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM productos WHERE id_producto = %s', (id_producto,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('productos'))


@app.route('/clientes')
def clientes_route():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT * FROM clientes')
    clientes_db = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('clientes.html', clientes=clientes_db)


@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def nuevo_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO clientes (nombre, sector, plan, estado) VALUES (%s, %s, %s, %s)',
            (form.nombre.data, form.sector.data, form.plan.data, form.estado.data)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('clientes_route'))
    return render_template('formulario_cliente.html', form=form)


@app.route('/facturacion')
def facturacion():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('''
        SELECT facturas.id_factura, facturas.numero, facturas.monto, facturas.estado,
               clientes.nombre AS cliente_nombre
        FROM facturas
        JOIN clientes ON facturas.id_cliente = clientes.id_cliente
    ''')
    facturas_db = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('facturacion.html', facturas=facturas_db)


@app.route('/facturacion/nueva', methods=['GET', 'POST'])
def nueva_factura():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT id_cliente, nombre FROM clientes')
    clientes_db = cursor.fetchall()
    cursor.close()

    form = FacturacionForm()
    form.id_cliente.choices = [(c['id_cliente'], c['nombre']) for c in clientes_db]

    if form.validate_on_submit():
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO facturas (numero, id_cliente, monto, estado) VALUES (%s, %s, %s, %s)',
            (form.numero.data, form.id_cliente.data, form.monto.data, form.estado.data)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('facturacion'))

    conn.close()
    return render_template('formulario_facturacion.html', form=form)


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
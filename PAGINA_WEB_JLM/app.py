from flask import Flask, render_template, request, redirect, url_for, flash
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from conexion.conexion import get_connection
from psycopg2.extras import RealDictCursor
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms.login_form import LoginForm
from forms.registro_form import RegistroForm
from models import Usuario

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jlmconnect360-clave-secreta-2026'
# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    """Carga un usuario desde la base de datos usando su ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, usuario, password FROM usuarios WHERE id = %s', (user_id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    if data:
        return Usuario(data[0], data[1], data[2])
    return None


@app.route('/')
def inicio():
    return render_template('index.html')


@app.route('/productos')
@login_required   
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
@login_required  
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
@login_required 
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


# ===================== PROVEEDORES =====================

@app.route('/proveedores')
@login_required  
def proveedores_route():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT id_proveedor, nombre, producto, contacto FROM proveedores')
    proveedores_db = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('proveedores.html', proveedores=proveedores_db)


@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
def nuevo_proveedor():
    form = ProveedorForm()
    if form.validate_on_submit():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO proveedores (nombre, producto, contacto) VALUES (%s, %s, %s)',
            (form.nombre.data, form.producto.data, form.contacto.data)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('proveedores_route'))
    return render_template('formulario_proveedor.html', form=form)


@app.route('/proveedores/editar/<int:id_proveedor>', methods=['GET', 'POST'])
def editar_proveedor(id_proveedor):
    conn = get_connection()
    cursor = conn.cursor()
    
    form = ProveedorForm()
    if form.validate_on_submit():
        cursor.execute(
            'UPDATE proveedores SET nombre = %s, producto = %s, contacto = %s WHERE id_proveedor = %s',
            (form.nombre.data, form.producto.data, form.contacto.data, id_proveedor)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('proveedores_route'))
    
    if request.method == 'GET':
        cursor.execute('SELECT nombre, producto, contacto FROM proveedores WHERE id_proveedor = %s', (id_proveedor,))
        proveedor = cursor.fetchone()
        if proveedor:
            form.nombre.data = proveedor[0]
            form.producto.data = proveedor[1]
            form.contacto.data = proveedor[2]
    
    cursor.close()
    conn.close()
    return render_template('formulario_proveedor.html', form=form, editar=True)


@app.route('/proveedores/eliminar/<int:id_proveedor>')
def eliminar_proveedor(id_proveedor):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM proveedores WHERE id_proveedor = %s', (id_proveedor,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('proveedores_route'))


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

# ===================== REGISTRO DE USUARIOS =====================

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """Registro de nuevos usuarios"""
    form = RegistroForm()
    if form.validate_on_submit():
        # Cifrar la contraseña antes de guardar
        password_hash = generate_password_hash(form.password.data)
        
        # Guardar en la base de datos
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO usuarios (usuario, password) VALUES (%s, %s)',
            (form.usuario.data, password_hash)
        )
        conn.commit()
        cursor.close()
        conn.close()
        
        # Mensaje de éxito
        flash('¡Usuario registrado exitosamente! Ahora puedes iniciar sesión.', 'success')
        
        # Redirigir al login
        return redirect(url_for('login'))
    
    return render_template('registro.html', form=form)


# ===================== LOGIN =====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Inicio de sesión"""
    form = LoginForm()
    error = None
    
    if form.validate_on_submit():
        # Buscar usuario en la base de datos
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, usuario, password FROM usuarios WHERE usuario = %s',
            (form.usuario.data,)
        )
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        
        # Verificar que existe y la contraseña es correcta
        if data and check_password_hash(data[2], form.password.data):
            user = Usuario(data[0], data[1], data[2])
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            error = "Usuario o contraseña incorrectos"
    
    return render_template('login.html', form=form, error=error)


# ===================== DASHBOARD (PÁGINA PROTEGIDA) =====================

@app.route('/dashboard')
@login_required
def dashboard():
    """Página de inicio (protegida - solo usuarios logueados)"""
    return render_template('dashboard.html', usuario=current_user.usuario)


# ===================== LOGOUT =====================

@app.route('/logout')
@login_required
def logout():
    """Cerrar sesión"""
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
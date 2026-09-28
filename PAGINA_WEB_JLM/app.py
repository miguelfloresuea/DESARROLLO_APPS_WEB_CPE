import os
from io import BytesIO
from datetime import datetime, timezone
from flask import make_response, flash, request
from xhtml2pdf import pisa
from flask import Flask, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from forms.login_form import LoginForm
from forms.registro_form import RegistroForm
from conexion.conexion import get_connection
from psycopg2.extras import RealDictCursor
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import Usuario

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jlmconnect360-clave-secreta-2026'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, usuario, password, nombre_completo FROM usuarios WHERE id = %s', (user_id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    if data:
        return Usuario(data[0], data[1], data[2], data[3])
    return None


@app.route('/')
def inicio():
    return render_template('index.html')


# ===================== PRODUCTOS =====================

@app.route('/productos')
@login_required
def productos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id_producto, nombre, velocidad, precio, descripcion FROM productos')
    filas = cursor.fetchall()
    cursor.close()
    conn.close()
    planes_db = [{"id_producto": f[0], "nombre": f[1], "velocidad": f[2], "precio": f[3], "descripcion": f[4]} for f in filas]
    return render_template('productos.html', 
                           planes=planes_db,
                           nombre_completo=current_user.nombre_completo)


@app.route('/productos/nuevo', methods=['GET', 'POST'])
@login_required
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
        flash('Producto registrado exitosamente.', 'success')
        return redirect(url_for('productos'))
    return render_template('formulario_producto.html', 
                           form=form,
                           nombre_completo=current_user.nombre_completo)


@app.route('/productos/editar/<int:id_producto>', methods=['GET', 'POST'])
@login_required
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
        flash('Producto actualizado correctamente.', 'success')
        return redirect(url_for('productos'))
    if request.method == 'GET':
        cursor.execute('SELECT nombre, velocidad, precio, descripcion FROM productos WHERE id_producto = %s', (id_producto,))
        producto = cursor.fetchone()
        if producto:
            form.nombre.data, form.velocidad.data, form.precio.data, form.descripcion.data = producto
    cursor.close()
    conn.close()
    return render_template('formulario_producto.html', 
                           form=form,
                           nombre_completo=current_user.nombre_completo)


@app.route('/productos/eliminar/<int:id_producto>')
@login_required
def eliminar_producto(id_producto):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM productos WHERE id_producto = %s', (id_producto,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Producto eliminado.', 'info')
    return redirect(url_for('productos'))


# ===================== CLIENTES =====================

@app.route('/clientes')
@login_required
def clientes_route():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('''
        SELECT c.id_cliente, c.nombre, c.ruc_cedula, c.celular, c.correo, 
               c.canton, c.ciudad, c.sector, c.plan, c.estado
        FROM clientes c
        ORDER BY c.nombre
    ''')
    clientes_db = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('clientes.html', 
                           clientes=clientes_db,
                           nombre_completo=current_user.nombre_completo)


@app.route('/clientes/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_cliente():
    form = ClienteForm()
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT id_producto, nombre, precio FROM productos ORDER BY nombre')
    productos_db = cursor.fetchall()
    form.id_producto.choices = [(p['id_producto'], f"{p['nombre']} - {p['precio']}/mes") for p in productos_db]
    cursor.close()
    conn.close()
    
    if form.validate_on_submit():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO clientes (nombre, ruc_cedula, celular, correo, canton, ciudad, sector, estado) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_cliente''',
            (form.nombre.data, form.ruc_cedula.data, form.celular.data, 
             form.correo.data, form.canton.data, form.ciudad.data, 
             form.sector.data, form.estado.data)
        )
        id_cliente = cursor.fetchone()[0]
        cursor.execute(
            '''INSERT INTO suscripciones (id_cliente, id_producto, estado) 
               VALUES (%s, %s, 'Activo')''',
            (id_cliente, form.id_producto.data)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('Cliente registrado exitosamente.', 'success')
        return redirect(url_for('clientes_route'))
    
    return render_template('formulario_cliente.html', 
                           form=form,
                           productos=productos_db,
                           nombre_completo=current_user.nombre_completo)


@app.route('/clientes/editar/<int:id_cliente>', methods=['GET', 'POST'])
@login_required
def editar_cliente(id_cliente):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT id_producto, nombre, precio FROM productos ORDER BY nombre')
    productos_db = cursor.fetchall()
    form = ClienteForm()
    form.id_producto.choices = [(p['id_producto'], f"{p['nombre']} - {p['precio']}/mes") for p in productos_db]
    
    if form.validate_on_submit():
        cursor2 = conn.cursor()
        cursor2.execute(
            '''UPDATE clientes SET nombre = %s, ruc_cedula = %s, celular = %s, 
               correo = %s, canton = %s, ciudad = %s, sector = %s, estado = %s
               WHERE id_cliente = %s''',
            (form.nombre.data, form.ruc_cedula.data, form.celular.data,
             form.correo.data, form.canton.data, form.ciudad.data,
             form.sector.data, form.estado.data, id_cliente)
        )
        conn.commit()
        cursor2.close()
        conn.close()
        flash('Cliente actualizado correctamente.', 'success')
        return redirect(url_for('clientes_route'))

    if request.method == 'GET':
        cursor.execute('''SELECT nombre, ruc_cedula, celular, correo, canton, ciudad, 
                                 sector, estado 
                          FROM clientes WHERE id_cliente = %s''', (id_cliente,))
        cliente = cursor.fetchone()
        if cliente:
            form.nombre.data = cliente['nombre']
            form.ruc_cedula.data = cliente['ruc_cedula']
            form.celular.data = cliente['celular']
            form.correo.data = cliente['correo']
            form.canton.data = cliente['canton']
            form.ciudad.data = cliente['ciudad']
            form.sector.data = cliente['sector']
            form.estado.data = cliente['estado']

    cursor.close()
    conn.close()
    return render_template('formulario_cliente.html', 
                           form=form, 
                           editar=True,
                           productos=productos_db,
                           nombre_completo=current_user.nombre_completo)


@app.route('/clientes/ver/<int:id_cliente>')
@login_required
def ver_cliente(id_cliente):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT * FROM clientes WHERE id_cliente = %s', (id_cliente,))
    cliente = cursor.fetchone()
    cursor.execute('''
        SELECT s.id_suscripcion, s.estado, s.fecha_inicio,
               p.nombre AS plan, p.precio, p.velocidad
        FROM suscripciones s
        JOIN productos p ON s.id_producto = p.id_producto
        WHERE s.id_cliente = %s
        ORDER BY s.fecha_inicio DESC
    ''', (id_cliente,))
    suscripciones = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('ver_cliente.html', 
                           cliente=cliente,
                           suscripciones=suscripciones,
                           nombre_completo=current_user.nombre_completo)


@app.route('/clientes/agregar-plan/<int:id_cliente>', methods=['GET', 'POST'])
@login_required
def agregar_plan_cliente(id_cliente):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    if request.method == 'POST':
        id_producto = request.form.get('id_producto')
        cursor.execute(
            '''INSERT INTO suscripciones (id_cliente, id_producto, estado) 
               VALUES (%s, %s, 'Activo')''',
            (id_cliente, id_producto)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('Plan agregado exitosamente.', 'success')
        return redirect(url_for('ver_cliente', id_cliente=id_cliente))
    cursor.execute('SELECT id_producto, nombre, precio FROM productos ORDER BY nombre')
    productos = cursor.fetchall()
    cursor.execute('SELECT nombre FROM clientes WHERE id_cliente = %s', (id_cliente,))
    cliente = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('agregar_plan.html', 
                           cliente=cliente,
                           productos=productos,
                           id_cliente=id_cliente,
                           nombre_completo=current_user.nombre_completo)


@app.route('/clientes/eliminar/<int:id_cliente>')
@login_required
def eliminar_cliente(id_cliente):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clientes WHERE id_cliente = %s', (id_cliente,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Cliente eliminado.', 'info')
    return redirect(url_for('clientes_route'))


# ===================== FACTURACIÓN =====================

MESES_ESP = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
    5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
    9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
}


@app.route('/facturacion')
@login_required
def facturacion():
    busqueda = request.args.get('busqueda', '')
    estado = request.args.get('estado', '')
    plan = request.args.get('plan', '')
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = '''
        SELECT f.id_factura, f.numero, f.monto, f.estado, f.forma_pago, 
               f.comprobante_pago, f.fecha_creacion,
               c.nombre AS cliente_nombre, c.id_cliente, c.plan AS cliente_plan,
               COALESCE(u.nombre_completo, u.usuario, 'Desconocido') AS registrado_por
        FROM facturas f
        JOIN clientes c ON f.id_cliente = c.id_cliente
        LEFT JOIN usuarios u ON f.id_usuario = u.id
        WHERE 1=1
    '''
    params = []
    if busqueda:
        query += """ AND (
            f.numero ILIKE %s 
            OR c.id_cliente::text = %s
            OR c.nombre ILIKE %s
        )"""
        params.extend([f"%{busqueda}%", busqueda, f"%{busqueda}%"])
    if estado:
        query += " AND f.estado = %s"
        params.append(estado)
    if plan:
        query += " AND c.plan = %s"
        params.append(plan)
    query += " ORDER BY f.numero DESC"
    cursor.execute(query, params)
    facturas_db = cursor.fetchall()
    ahora = datetime.now()
    for factura in facturas_db:
        fecha_creacion = factura.get('fecha_creacion')
        if fecha_creacion:
            if fecha_creacion.tzinfo is None:
                diff_horas = (ahora - fecha_creacion).total_seconds() / 3600
            else:
                ahora_tz = ahora.replace(tzinfo=timezone.utc)
                diff_horas = (ahora_tz - fecha_creacion).total_seconds() / 3600
            factura['editable'] = diff_horas <= 24
        else:
            factura['editable'] = False
    cursor.close()
    conn.close()
    return render_template('facturacion.html', 
                           facturas=facturas_db, 
                           busqueda=busqueda, 
                           estado=estado, 
                           plan=plan,
                           nombre_completo=current_user.nombre_completo)


@app.route('/facturacion/nueva', methods=['GET', 'POST'])
@login_required
def nueva_factura():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT id_cliente, nombre FROM clientes ORDER BY nombre')
    clientes_db = cursor.fetchall()
    cursor.execute('SELECT id_producto, nombre, precio FROM productos ORDER BY nombre')
    productos_db = cursor.fetchall()
    cursor.execute("SELECT numero FROM facturas ORDER BY id_factura DESC LIMIT 1")
    ultima_factura = cursor.fetchone()
    if ultima_factura and ultima_factura['numero']:
        try:
            partes = ultima_factura['numero'].split('-')
            if len(partes) == 2:
                siguiente_numero = int(partes[1]) + 1
            else:
                siguiente_numero = 1
        except:
            siguiente_numero = 1
    else:
        siguiente_numero = 1
    numero_factura = f"F001-{siguiente_numero:06d}"
    cursor.close()
    form = FacturacionForm()
    form.id_cliente.choices = [(c['id_cliente'], f"[{c['id_cliente']}] {c['nombre']}") for c in clientes_db]
    form.id_producto.choices = [(p['id_producto'], f"{p['nombre']} - {p['precio']}") for p in productos_db]
    if form.validate_on_submit():
        cursor = conn.cursor()
        cursor.execute('SELECT precio FROM productos WHERE id_producto = %s', (form.id_producto.data,))
        producto_sel = cursor.fetchone()
        precio_str = producto_sel[0] if producto_sel else '0.00'
        precio_con_iva = float(precio_str.replace('$', '').strip())
        comprobante_path = None
        if form.comprobante_pago.data and form.comprobante_pago.data.filename:
            carpeta_comprobantes = os.path.join(app.root_path, 'static', 'comprobantes')
            os.makedirs(carpeta_comprobantes, exist_ok=True)
            filename = secure_filename(f"comp_{numero_factura}_{form.comprobante_pago.data.filename}")
            filepath = os.path.join(carpeta_comprobantes, filename)
            form.comprobante_pago.data.save(filepath)
            comprobante_path = f"comprobantes/{filename}"
        cursor.execute(
            '''INSERT INTO facturas (numero, id_cliente, monto, estado, id_usuario, forma_pago, comprobante_pago, fecha_creacion)
               VALUES (%s, %s, %s, %s, %s, %s, %s, NOW()) RETURNING id_factura''',
            (numero_factura, form.id_cliente.data, precio_str, form.estado.data, 
             current_user.id, form.forma_pago.data, comprobante_path)
        )
        id_factura_nueva = cursor.fetchone()[0]
        subtotal_sin_iva = round(precio_con_iva / 1.15, 2)
        iva = round(precio_con_iva - subtotal_sin_iva, 2)
        cursor.execute(
            '''INSERT INTO detalle_factura (id_factura, id_producto, cantidad, precio_unitario, subtotal)
               VALUES (%s, %s, 1, %s, %s)''',
            (id_factura_nueva, form.id_producto.data, subtotal_sin_iva, subtotal_sin_iva)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash(f'Factura {numero_factura} registrada exitosamente.', 'success')
        return redirect(url_for('facturacion'))
    conn.close()
    return render_template('formulario_facturacion.html', 
                           form=form, 
                           numero_factura=numero_factura,
                           nombre_completo=current_user.nombre_completo)


@app.route('/facturacion/editar/<int:id_factura>', methods=['GET', 'POST'])
@login_required
def editar_factura(id_factura):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('''
        SELECT id_factura, numero, id_cliente, monto, estado, forma_pago, fecha_creacion
        FROM facturas WHERE id_factura = %s
    ''', (id_factura,))
    factura_data = cursor.fetchone()
    if not factura_data:
        flash('Factura no encontrada.', 'danger')
        cursor.close()
        conn.close()
        return redirect(url_for('facturacion'))
    if factura_data['estado'] == 'Anulada':
        flash('No se puede editar una factura anulada.', 'danger')
        cursor.close()
        conn.close()
        return redirect(url_for('facturacion'))
    fecha_creacion = factura_data['fecha_creacion']
    if fecha_creacion:
        if fecha_creacion.tzinfo is None:
            diff_horas = (datetime.now() - fecha_creacion).total_seconds() / 3600
        else:
            ahora_tz = datetime.now().replace(tzinfo=timezone.utc)
            diff_horas = (ahora_tz - fecha_creacion).total_seconds() / 3600
        if diff_horas > 24:
            flash('Solo se pueden editar facturas dentro de las 24 horas de su creación.', 'warning')
            cursor.close()
            conn.close()
            return redirect(url_for('facturacion'))
    cursor.execute('SELECT id_cliente, nombre FROM clientes')
    clientes_db = cursor.fetchall()
    cursor.execute('SELECT id_producto, nombre, precio FROM productos')
    productos_db = cursor.fetchall()
    form = FacturacionForm()
    form.id_cliente.choices = [(c['id_cliente'], f"[{c['id_cliente']}] {c['nombre']}") for c in clientes_db]
    form.id_producto.choices = [(p['id_producto'], f"{p['nombre']} - {p['precio']}") for p in productos_db]
    if form.validate_on_submit():
        cursor2 = conn.cursor()
        comprobante_path = None
        if form.comprobante_pago.data and form.comprobante_pago.data.filename:
            carpeta_comprobantes = os.path.join(app.root_path, 'static', 'comprobantes')
            os.makedirs(carpeta_comprobantes, exist_ok=True)
            filename = secure_filename(f"comp_edit_{id_factura}_{form.comprobante_pago.data.filename}")
            filepath = os.path.join(carpeta_comprobantes, filename)
            form.comprobante_pago.data.save(filepath)
            comprobante_path = f"comprobantes/{filename}"
        if comprobante_path:
            cursor2.execute(
                'UPDATE facturas SET estado = %s, forma_pago = %s, comprobante_pago = %s WHERE id_factura = %s',
                (form.estado.data, form.forma_pago.data, comprobante_path, id_factura)
            )
        else:
            cursor2.execute(
                'UPDATE facturas SET estado = %s, forma_pago = %s WHERE id_factura = %s',
                (form.estado.data, form.forma_pago.data, id_factura)
            )
        conn.commit()
        cursor2.close()
        conn.close()
        flash('Factura actualizada correctamente.', 'success')
        return redirect(url_for('facturacion'))
    if request.method == 'GET':
        form.id_cliente.data = factura_data['id_cliente']
        form.estado.data = factura_data['estado']
        form.forma_pago.data = factura_data.get('forma_pago', 'Efectivo')
    cursor.close()
    conn.close()
    return render_template('formulario_facturacion.html', 
                           form=form, 
                           editar=True, 
                           numero_factura=factura_data['numero'],
                           nombre_completo=current_user.nombre_completo)


@app.route('/facturacion/anular/<int:id_factura>', methods=['GET', 'POST'])
@login_required
def anular_factura(id_factura):
    if request.method == 'POST':
        motivo = request.form.get('motivo', '')
        observaciones = request.form.get('observaciones', '')
        if not motivo:
            flash('Debe seleccionar un motivo de anulación.', 'danger')
            return redirect(url_for('facturacion'))
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE facturas SET estado = %s, motivo_anulacion = %s, observaciones_anulacion = %s WHERE id_factura = %s",
            ('Anulada', motivo, observaciones, id_factura)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('Factura anulada correctamente.', 'info')
        return redirect(url_for('facturacion'))
    return redirect(url_for('facturacion'))


@app.route('/facturacion/pdf/<int:id_factura>')
@login_required
def factura_pdf(id_factura):
    """Generar PDF de la factura con sello ANULADA (solo texto, sin rectángulo)"""
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    cursor.execute('''
        SELECT f.id_factura, f.numero, f.monto, f.estado, f.forma_pago, f.fecha_creacion,
               f.motivo_anulacion, f.observaciones_anulacion,
               c.nombre AS cliente_nombre, c.sector AS cliente_sector,
               c.ruc_cedula AS cliente_ruc, c.celular AS cliente_celular, c.correo AS cliente_correo,
               c.canton AS cliente_canton, c.ciudad AS cliente_ciudad,
               COALESCE(u.nombre_completo, u.usuario) AS registrado_por
        FROM facturas f
        JOIN clientes c ON f.id_cliente = c.id_cliente
        LEFT JOIN usuarios u ON f.id_usuario = u.id
        WHERE f.id_factura = %s
    ''', (id_factura,))
    factura = cursor.fetchone()

    cursor.execute('''
        SELECT p.nombre, p.velocidad, p.descripcion, df.cantidad, df.precio_unitario, df.subtotal
        FROM detalle_factura df
        JOIN productos p ON df.id_producto = p.id_producto
        WHERE df.id_factura = %s
    ''', (id_factura,))
    detalle = cursor.fetchall()
    
    fecha = factura['fecha_creacion'] if factura['fecha_creacion'] else datetime.now()
    periodo = f"{MESES_ESP[fecha.month]} {fecha.year}"
    fecha_emision = fecha.strftime('%d/%m/%Y')
    fecha_autorizacion = fecha.strftime('%d/%m/%Y %H:%M:%S')
    
    if detalle:
        total = sum(float(d['subtotal']) for d in detalle)
    else:
        monto_str = factura['monto'] if factura['monto'] else '0.00'
        total = float(monto_str.replace('$', '').strip())
    
    subtotal_sin_iva = round(total / 1.15, 2)
    iva = round(total - subtotal_sin_iva, 2)
    
    detalle_preparado = []
    for item in detalle:
        descripcion = item['nombre']
        if item.get('velocidad'):
            descripcion += f" - {item['velocidad']}"
        if item.get('descripcion'):
            descripcion += f" ({item['descripcion']})"
        precio_con_iva = float(item['precio_unitario'])
        subtotal_con_iva = round(precio_con_iva * item['cantidad'], 2)
        detalle_preparado.append({
            'descripcion_completa': descripcion,
            'cantidad': item['cantidad'],
            'precio_unitario': precio_con_iva,
            'subtotal': subtotal_con_iva
        })
    
    if not detalle_preparado:
        monto_str = factura['monto'] if factura['monto'] else '0.00'
        precio_total = float(monto_str.replace('$', '').strip())
        detalle_preparado.append({
            'descripcion_completa': 'Servicio de Internet (ver monto total)',
            'cantidad': 1,
            'precio_unitario': precio_total,
            'subtotal': precio_total
        })
    
    factura['periodo'] = periodo
    factura['fecha_emision'] = fecha_emision
    factura['fecha_autorizacion'] = fecha_autorizacion
    factura['subtotal_sin_iva'] = subtotal_sin_iva
    factura['iva'] = iva
    factura['total'] = total
    
    cursor.close()
    conn.close()

    logo_path = os.path.join(app.root_path, 'static', 'img', 'LOGO.png').replace('\\', '/')
    html = render_template('factura_pdf.html', factura=factura, detalle=detalle_preparado, logo_path=logo_path)

    # Generar PDF base con xhtml2pdf
    pdf_buffer = BytesIO()
    pisa.CreatePDF(html, dest=pdf_buffer)
    pdf_buffer.seek(0)
    
    # Si está anulada, agregar sello con ReportLab (SOLO TEXTO, sin rectángulo)
    if factura['estado'] == 'Anulada':
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas
            from reportlab.lib.colors import red
            from PyPDF2 import PdfReader, PdfWriter
            
            reader = PdfReader(pdf_buffer)
            writer = PdfWriter()
            
            sello_buffer = BytesIO()
            c = canvas.Canvas(sello_buffer, pagesize=A4)
            
            page_width, page_height = A4
            
            c.saveState()
            c.translate(page_width / 2, page_height / 2)
            c.rotate(-35)
            
            # SOLO el texto ANULADA, sin rectángulo
            c.setFillColor(red)
            c.setFont("Helvetica-Bold", 90)
            c.setFillAlpha(0.4)
            c.drawCentredString(0, 0, "ANULADA")
            
            c.restoreState()
            c.save()
            
            sello_buffer.seek(0)
            sello_reader = PdfReader(sello_buffer)
            sello_page = sello_reader.pages[0]
            
            for page in reader.pages:
                page.merge_page(sello_page)
                writer.add_page(page)
            
            pdf_final = BytesIO()
            writer.write(pdf_final)
            pdf_final.seek(0)
            pdf_buffer = pdf_final
            
        except Exception as e:
            print(f"Error al agregar sello: {e}")
            pdf_buffer.seek(0)
    
    response = make_response(pdf_buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=factura_{factura["numero"]}.pdf'
    return response


@app.route('/facturacion/reportes')
@login_required
def reportes_facturacion():
    fecha_inicio = request.args.get('fecha_inicio', '')
    fecha_fin = request.args.get('fecha_fin', '')
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query_stats = '''
        SELECT COUNT(*) as total, 
               SUM(CASE WHEN estado = 'Pagada' THEN REPLACE(monto, '$', '')::NUMERIC ELSE 0 END) as total_pagado, 
               SUM(CASE WHEN estado = 'Pendiente' THEN REPLACE(monto, '$', '')::NUMERIC ELSE 0 END) as total_pendiente 
        FROM facturas WHERE 1=1
    '''
    query_top = '''
        SELECT c.nombre, COUNT(f.id_factura) as cantidad, 
               SUM(REPLACE(f.monto, '$', '')::NUMERIC) as total
        FROM facturas f
        JOIN clientes c ON f.id_cliente = c.id_cliente
        WHERE f.estado = 'Pagada'
    '''
    params_stats = []
    params_top = []
    if fecha_inicio:
        query_stats += " AND fecha_creacion >= %s"
        query_top += " AND f.fecha_creacion >= %s"
        params_stats.append(fecha_inicio)
        params_top.append(fecha_inicio)
    if fecha_fin:
        query_stats += " AND fecha_creacion < %s::date + 1"
        query_top += " AND f.fecha_creacion < %s::date + 1"
        params_stats.append(fecha_fin)
        params_top.append(fecha_fin)
    query_top += " GROUP BY c.nombre ORDER BY total DESC LIMIT 5"
    cursor.execute(query_stats, params_stats)
    stats = cursor.fetchone()
    cursor.execute(query_top, params_top)
    top_clientes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template(
        'reportes_facturacion.html', 
        stats=stats, 
        top_clientes=top_clientes,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        nombre_completo=current_user.nombre_completo
    )


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
    return render_template('proveedores.html', 
                           proveedores=proveedores_db,
                           nombre_completo=current_user.nombre_completo)


@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
@login_required
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
        flash('Proveedor registrado exitosamente.', 'success')
        return redirect(url_for('proveedores_route'))
    return render_template('formulario_proveedor.html', 
                           form=form,
                           nombre_completo=current_user.nombre_completo)


@app.route('/proveedores/editar/<int:id_proveedor>', methods=['GET', 'POST'])
@login_required
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
        flash('Proveedor actualizado correctamente.', 'success')
        return redirect(url_for('proveedores_route'))
    if request.method == 'GET':
        cursor.execute('SELECT nombre, producto, contacto FROM proveedores WHERE id_proveedor = %s', (id_proveedor,))
        proveedor = cursor.fetchone()
        if proveedor:
            form.nombre.data, form.producto.data, form.contacto.data = proveedor
    cursor.close()
    conn.close()
    return render_template('formulario_proveedor.html', 
                           form=form, 
                           editar=True,
                           nombre_completo=current_user.nombre_completo)


@app.route('/proveedores/eliminar/<int:id_proveedor>')
@login_required
def eliminar_proveedor(id_proveedor):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM proveedores WHERE id_proveedor = %s', (id_proveedor,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Proveedor eliminado.', 'info')
    return redirect(url_for('proveedores_route'))


# ===================== CONTACTO =====================

@app.route('/contacto', methods=['POST'])
def procesar_contacto():
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    asunto = request.form.get('asunto')
    mensaje = request.form.get('mensaje')
    return render_template('confirmacion.html', 
                           nombre=nombre, 
                           email=email, 
                           asunto=asunto, 
                           mensaje=mensaje)


# ===================== REGISTRO DE USUARIOS =====================

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()
    if form.validate_on_submit():
        password_hash = generate_password_hash(form.password.data)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO usuarios (usuario, password, nombre_completo) VALUES (%s, %s, %s)',
            (form.usuario.data, password_hash, form.nombre_completo.data)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('¡Usuario registrado exitosamente! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))
    return render_template('registro.html', form=form)


# ===================== LOGIN =====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, usuario, password, nombre_completo FROM usuarios WHERE usuario = %s', (form.usuario.data,))
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        if data and check_password_hash(data[2], form.password.data):
            user = Usuario(data[0], data[1], data[2], data[3])
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            error = "Usuario o contraseña incorrectos"
    return render_template('login.html', form=form, error=error)


# ===================== DASHBOARD =====================

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', 
                           usuario=current_user.usuario, 
                           nombre_completo=current_user.nombre_completo)


# ===================== LOGOUT =====================

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

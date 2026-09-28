from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, FileField
from wtforms.validators import DataRequired, ValidationError
from werkzeug.utils import secure_filename
import os


def allowed_file(filename):
    """Valida que el archivo sea PDF"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'


class FacturacionForm(FlaskForm):
    id_cliente = SelectField('Cliente', coerce=int, validators=[DataRequired()])
    id_producto = SelectField('Plan / Servicio', coerce=int, validators=[DataRequired()])
    forma_pago = SelectField('Forma de Pago', choices=[
        ('Efectivo', 'Efectivo'),
        ('Transferencia', 'Transferencia'),
        ('Deposito', 'Depósito')
    ], validators=[DataRequired()])
    comprobante_pago = FileField('Comprobante de Pago (PDF)', validators=[])
    estado = SelectField('Estado', choices=[
        ('Pendiente', 'Pendiente'),
        ('Pagada', 'Pagada'),
        ('Anulada', 'Anulada')
    ], validators=[DataRequired()])
    submit = SubmitField('Guardar Factura')

    def validate_comprobante_pago(self, field):
        """Valida que si es Transferencia o Depósito, se suba un PDF"""
        forma_pago = self.forma_pago.data
        if forma_pago in ['Transferencia', 'Deposito']:
            if not field.data or not field.data.filename:
                raise ValidationError('Debe subir el comprobante de pago en PDF para Transferencia o Depósito.')
            if not allowed_file(field.data.filename):
                raise ValidationError('El comprobante debe ser un archivo PDF.')


class AnulacionForm(FlaskForm):
    """Formulario para capturar el motivo de anulación"""
    motivo = SelectField('Motivo de Anulación', choices=[
        ('error_emision', 'Error en la emisión del comprobante'),
        ('devolucion', 'Devolución de bienes o servicios'),
        ('cancelacion_venta', 'Cancelación de la venta antes de la entrega'),
        ('otro', 'Otro (especificar en observaciones)')
    ], validators=[DataRequired()])
    observaciones = SelectField('Observaciones adicionales (opcional)', choices=[
        ('', '-- Sin observaciones --'),
        ('datos_cliente_incorrectos', 'Datos del cliente incorrectos'),
        ('monto_erroneo', 'Monto incorrecto'),
        ('producto_no_entregado', 'Producto/Servicio no entregado'),
        ('cliente_solicito', 'Solicitud del cliente'),
        ('duplicado', 'Factura duplicada')
    ])
    submit = SubmitField('Confirmar Anulación')
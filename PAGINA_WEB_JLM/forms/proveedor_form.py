from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class ProveedorForm(FlaskForm):
    nombre = StringField('Nombre del Proveedor', validators=[DataRequired(), Length(min=3, max=80)])
    producto = StringField('Producto / Servicio', validators=[DataRequired()])
    contacto = StringField('Correo de Contacto', validators=[DataRequired(), Email()])
    submit = SubmitField('Guardar Proveedor')
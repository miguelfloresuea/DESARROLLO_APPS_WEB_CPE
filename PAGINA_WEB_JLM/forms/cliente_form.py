from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length

CANTONES_MORONA_SANTIAGO = [
    ('Morona', 'Morona'),
    ('Gualaquiza', 'Gualaquiza'),
    ('Limón Indanza', 'Limón Indanza'),
    ('Palora', 'Palora'),
    ('Santiago', 'Santiago'),
    ('Sucúa', 'Sucúa'),
    ('Huamboya', 'Huamboya'),
    ('San Juan Bosco', 'San Juan Bosco'),
    ('Taisha', 'Taisha'),
    ('Logroño', 'Logroño'),
    ('Pablo Sexto', 'Pablo Sexto'),
    ('Tiwintza', 'Tiwintza')
]

class ClienteForm(FlaskForm):
    nombre = StringField('Nombre Completo', validators=[DataRequired(), Length(min=3, max=100)])
    ruc_cedula = StringField('RUC / Cédula', validators=[DataRequired(), Length(min=10, max=13)])
    celular = StringField('Celular', validators=[DataRequired(), Length(min=10, max=10)])
    correo = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    
    canton = SelectField('Cantón', choices=CANTONES_MORONA_SANTIAGO, validators=[DataRequired()])
    ciudad = StringField('Ciudad / Parroquia / Barrio', validators=[DataRequired()])
    sector = StringField('Dirección detallada (calle principal y secundaria)', validators=[DataRequired()])
    
    id_producto = SelectField('Plan', coerce=int, validators=[DataRequired()])
    
    estado = SelectField('Estado', choices=[
        ('Activo', 'Activo'),
        ('Pendiente instalación', 'Pendiente instalación'),
        ('Suspendido', 'Suspendido')
    ], validators=[DataRequired()])
    
    submit = SubmitField('Guardar Cliente')
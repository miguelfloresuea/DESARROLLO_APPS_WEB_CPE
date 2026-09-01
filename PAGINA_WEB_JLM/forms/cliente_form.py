from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length


class ClienteForm(FlaskForm):
    nombre = StringField('Nombre del Cliente', validators=[DataRequired(), Length(min=3, max=80)])
    sector = StringField('Sector', validators=[DataRequired()])
    plan = SelectField('Plan', choices=[
        ('Residencial', 'Residencial'),
        ('Empresarial', 'Empresarial'),
        ('Educativo', 'Educativo'),
        ('Rural', 'Rural')
    ], validators=[DataRequired()])
    estado = SelectField('Estado', choices=[
        ('Activo', 'Activo'),
        ('Pendiente instalación', 'Pendiente instalación')
    ], validators=[DataRequired()])
    submit = SubmitField('Guardar Cliente')
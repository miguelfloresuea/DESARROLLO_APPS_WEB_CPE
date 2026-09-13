from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length


class FacturacionForm(FlaskForm):
    numero = StringField('N° Factura', validators=[DataRequired(), Length(min=5)])
    id_cliente = SelectField('Cliente', coerce=int, validators=[DataRequired()])
    monto = StringField('Monto', validators=[DataRequired()])
    estado = StringField('Estado', validators=[DataRequired()])
    submit = SubmitField('Guardar Factura')
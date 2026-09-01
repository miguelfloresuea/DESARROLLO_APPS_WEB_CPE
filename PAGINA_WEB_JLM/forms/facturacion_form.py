from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class FacturacionForm(FlaskForm):
    numero = StringField('N° Factura', validators=[DataRequired(), Length(min=5)])
    cliente = StringField('Cliente', validators=[DataRequired()])
    monto = StringField('Monto', validators=[DataRequired()])
    estado = StringField('Estado', validators=[DataRequired()])
    submit = SubmitField('Guardar Factura')
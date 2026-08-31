from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class ProductoForm(FlaskForm):
    nombre = StringField('Nombre del Plan', validators=[DataRequired(), Length(min=3, max=50)])
    velocidad = StringField('Velocidad', validators=[DataRequired()])
    precio = StringField('Precio', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Guardar Plan')
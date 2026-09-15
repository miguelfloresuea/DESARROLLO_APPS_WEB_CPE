from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
import re

def validate_password_strength(form, field):
    """Valida que la contraseña tenga requisitos de seguridad"""
    password = field.data
    
    if len(password) < 6:
        raise ValidationError('Mínimo 6 caracteres')
    
    if not re.search(r'[A-Z]', password):
        raise ValidationError('Debe tener al menos 1 mayúscula')
    
    if not re.search(r'[a-z]', password):
        raise ValidationError('Debe tener al menos 1 minúscula')
    
    if not re.search(r'\d', password):
        raise ValidationError('Debe tener al menos 1 número')
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError('Debe tener al menos 1 símbolo (!@#$%^&*)')


class RegistroForm(FlaskForm):
    usuario = StringField('Usuario', validators=[
        DataRequired(message='El usuario es obligatorio'),
        Length(min=3, max=50, message='Entre 3 y 50 caracteres')
    ])
    
    password = PasswordField('Contraseña', validators=[
        DataRequired(message='La contraseña es obligatoria'),
        validate_password_strength
    ])
    
    submit = SubmitField('Registrarse')
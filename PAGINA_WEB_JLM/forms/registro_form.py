from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from models import Usuario


class RegistroForm(FlaskForm):
    usuario = StringField('Usuario', validators=[
        DataRequired(message='El usuario es obligatorio'),
        Length(min=3, max=50, message='El usuario debe tener entre 3 y 50 caracteres')
    ])
    nombre_completo = StringField('Nombre Completo', validators=[
        DataRequired(message='El nombre completo es obligatorio'),
        Length(min=3, max=100, message='El nombre debe tener entre 3 y 100 caracteres')
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(message='La contraseña es obligatoria'),
        Length(min=6, message='La contraseña debe tener al menos 6 caracteres')
    ])
    confirmar_password = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(message='Debes confirmar la contraseña'),
        EqualTo('password', message='Las contraseñas no coinciden')
    ])
    submit = SubmitField('Registrarse')

    def validate_usuario(self, usuario):
        """Verifica que el usuario no exista ya en la base de datos"""
        from conexion.conexion import get_connection
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM usuarios WHERE usuario = %s', (usuario.data,))
        existe = cursor.fetchone()
        cursor.close()
        conn.close()
        if existe:
            raise ValidationError('Este nombre de usuario ya está en uso. Elige otro.')
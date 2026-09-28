from flask_login import UserMixin

class Usuario(UserMixin):
    def __init__(self, id, usuario, password, nombre_completo=None):
        self.id = id
        self.usuario = usuario
        self.password = password
        self.nombre_completo = nombre_completo
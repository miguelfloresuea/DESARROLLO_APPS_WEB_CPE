from flask_login import UserMixin

ROLES_PERMISOS = {
    'Supervisor': {
        'clientes_crear': True, 'clientes_editar': True, 'clientes_eliminar': False,
        'proveedores_crear': True, 'proveedores_editar': True, 'proveedores_eliminar': False,
        'planes_crear': True, 'planes_editar': True, 'planes_eliminar': False,
        'facturas_editar': True, 'facturas_anular': True
    },
    'Ventas': {
        'clientes_crear': True, 'clientes_editar': True, 'clientes_eliminar': False,
        'proveedores_crear': False, 'proveedores_editar': False, 'proveedores_eliminar': False,
        'planes_crear': False, 'planes_editar': False, 'planes_eliminar': False,
        'facturas_editar': False, 'facturas_anular': False
    },
    'Tecnico': {
        'clientes_crear': False, 'clientes_editar': False, 'clientes_eliminar': False,
        'proveedores_crear': False, 'proveedores_editar': False, 'proveedores_eliminar': False,
        'planes_crear': False, 'planes_editar': False, 'planes_eliminar': False,
        'facturas_editar': False, 'facturas_anular': False
    }
}

class Usuario(UserMixin):
    def __init__(self, id, usuario, password, nombre_completo=None, es_admin=False, rol='Ventas', activo=True):
        self.id = id
        self.usuario = usuario
        self.password = password
        self.nombre_completo = nombre_completo
        self.es_admin = es_admin
        self.rol = rol
        self.activo = activo
        
        if self.es_admin:
            permisos = {k: True for k in ROLES_PERMISOS['Supervisor'].keys()}
        else:
            permisos = ROLES_PERMISOS.get(rol, {})

        self.clientes_crear = permisos.get('clientes_crear', False)
        self.clientes_editar = permisos.get('clientes_editar', False)
        self.clientes_eliminar = permisos.get('clientes_eliminar', False)
        self.proveedores_crear = permisos.get('proveedores_crear', False)
        self.proveedores_editar = permisos.get('proveedores_editar', False)
        self.proveedores_eliminar = permisos.get('proveedores_eliminar', False)
        self.planes_crear = permisos.get('planes_crear', False)
        self.planes_editar = permisos.get('planes_editar', False)
        self.planes_eliminar = permisos.get('planes_eliminar', False)
        self.facturas_editar = permisos.get('facturas_editar', False)
        self.facturas_anular = permisos.get('facturas_anular', False)
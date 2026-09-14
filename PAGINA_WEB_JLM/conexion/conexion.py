import psycopg2
from conexion.config_local import PASSWORD

# La contrasena de PostgreSQL NO se guarda directamente en este archivo.
# Cada integrante del equipo tiene su propio archivo conexion/config_local.py
# con su contrasena local, el cual esta excluido del repositorio mediante .gitignore.
# Esto evita subir credenciales reales a GitHub y permite que cada quien use
# su propia base de datos local sin sobreescribir la de los demas.
# Ver conexion/config_local.example.py para el formato esperado de ese archivo.


def get_connection():
    return psycopg2.connect(
        host='localhost',
        port='5432',
        dbname='jlmconnect',
        user='postgres',
        password=PASSWORD
    )
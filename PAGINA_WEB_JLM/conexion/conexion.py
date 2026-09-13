# Este archivo centraliza la conexion a la base de datos PostgreSQL de JLM Connect 360
import psycopg2


def get_connection():
    return psycopg2.connect(
        host='localhost',
        port='5432',
        dbname='jlmconnect',
        user='postgres',
        password='12345678.A'
    )
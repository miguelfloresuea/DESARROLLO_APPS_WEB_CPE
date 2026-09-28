import os
import psycopg2

def get_connection():
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        return psycopg2.connect(database_url, sslmode='require')
    else:
        from conexion.config_local import HOST, USER, PASSWORD, DATABASE, PORT
        return psycopg2.connect(
            host=HOST,
            port=PORT,
            dbname=DATABASE,
            user=USER,
            password=PASSWORD
        )
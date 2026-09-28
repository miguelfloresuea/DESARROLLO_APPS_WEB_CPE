import os
import psycopg2

def get_connection():
    # Render le enviará la URL de la base de datos automáticamente
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        # Si está en Render, usa la base de datos de la nube
        return psycopg2.connect(database_url)
    else:
        # Si estás en tu laptop, usa tu base de datos local
        return psycopg2.connect(
            host='localhost',
            database='jlmconnect',
            user='postgres',
            password='Angel1990P' # Pon tu contraseña de tu PostgreSQL local
        )
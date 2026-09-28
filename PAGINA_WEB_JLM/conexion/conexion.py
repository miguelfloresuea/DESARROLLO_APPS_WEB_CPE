import os
import psycopg2
from dotenv import load_dotenv

# Carga las variables del archivo .env en tu entorno local.
# En Render, esto no interfiere porque usará sus propias variables de entorno.
load_dotenv()

def get_connection():
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        return psycopg2.connect(database_url)
    else:
        return psycopg2.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            database=os.environ.get('DB_NAME', 'jlmconnect'),
            user=os.environ.get('DB_USER', 'postgres'),
            password=os.environ.get('DB_PASSWORD') 
        )

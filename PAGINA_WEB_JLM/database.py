import sqlite3
import os

os.makedirs('data', exist_ok=True)
DB_PATH = os.path.join('data', 'jlmconnect.db')


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            velocidad TEXT NOT NULL,
            precio TEXT NOT NULL,
            descripcion TEXT NOT NULL
        )
    ''')

    cursor.execute('SELECT COUNT(*) FROM productos')
    if cursor.fetchone()[0] == 0:
        planes_iniciales = [
            ("Plan Residencial", "20 Mbps", "$18.00", "Ideal para navegación, streaming y videollamadas familiares."),
            ("Plan Empresarial", "50 Mbps simétrico", "$45.00", "Conexión de alta velocidad y estabilidad para negocios."),
            ("Plan Educativo", "15 Mbps", "$12.00", "Tarifa preferencial para instituciones educativas."),
            ("Plan Rural", "10 Mbps", "$15.00", "Cobertura mediante enlaces punto a multipunto de 5 GHz."),
        ]
        cursor.executemany(
            'INSERT INTO productos (nombre, velocidad, precio, descripcion) VALUES (?, ?, ?, ?)',
            planes_iniciales
        )

    conn.commit()
    conn.close()
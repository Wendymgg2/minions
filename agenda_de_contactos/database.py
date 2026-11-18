
import sqlite3

def conectar():
    conexion = sqlite3.connect("contactos.db")
    conexion.row_factory = sqlite3.Row
    return conexion


def crear_tabla():
    conexion = conectar()

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS contactos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            correo TEXT,
            categoria TEXT NOT NULL,
            avatar TEXT DEFAULT 'kevin'
        )
    """)

    # Revisar si la columna avatar ya existe
    columnas = conexion.execute(
        "PRAGMA table_info(contactos)"
    ).fetchall()

    nombres_columnas = [columna["name"] for columna in columnas]

    # Agregar avatar si se está usando una base de datos anterior
    if "avatar" not in nombres_columnas:
        conexion.execute("""
            ALTER TABLE contactos
            ADD COLUMN avatar TEXT DEFAULT 'kevin'
        """)
        conexion.commit()
        conexion.close()
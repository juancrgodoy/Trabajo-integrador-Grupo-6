import sqlite3

def crear_tabla():
    conn = sqlite3.connect('imagenes.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ruta_original TEXT,
            resolucion TEXT,
            profundidad TEXT,
            fecha TEXT
        )
    """)
    conn.commit()
    conn.close()

def guardar_proceso(ruta, resolucion, profundidad, fecha):
    conn = sqlite3.connect('imagenes.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO historico (ruta_original, resolucion, profundidad, fecha)
        VALUES (?, ?, ?, ?)
    """, (ruta, resolucion, profundidad, fecha))
    conn.commit()
    conn.close()

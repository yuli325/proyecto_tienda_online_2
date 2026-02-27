import sqlite3

# Conexión a la base de datos
def conectar():
    return sqlite3.connect("tienda.db")

# Crear tabla productos
def crear_tabla():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()

# Insertar un nuevo producto
def insertar_producto(nombre, cantidad, precio):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)",
        (nombre, cantidad, precio)
    )

    conexion.commit()
    conexion.close()

# Obtener todos los productos
def obtener_productos():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    conexion.close()
    return productos

# Eliminar un producto por id
def eliminar_producto(id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
    conexion.commit()
    conexion.close()

# Actualizar producto por id
def actualizar_producto(id, cantidad, precio):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        "UPDATE productos SET cantidad = ?, precio = ? WHERE id = ?",
        (cantidad, precio, id)
    )
    conexion.commit()
    conexion.close()
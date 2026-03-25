from conexion.conexion import obtener_conexion

def obtener_productos():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    datos = cursor.fetchall()
    conn.close()
    return datos

def obtener_producto(id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE id_producto=%s", (id,))
    dato = cursor.fetchone()
    conn.close()
    return dato

def crear_producto(nombre, precio, stock):
    conn = obtener_conexion()
    cursor = conn.cursor()
    sql = "INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)"
    cursor.execute(sql, (nombre, precio, stock))
    conn.commit()
    conn.close()

def actualizar_producto(id, nombre, precio, stock):
    conn = obtener_conexion()
    cursor = conn.cursor()
    sql = "UPDATE productos SET nombre=%s, precio=%s, stock=%s WHERE id_producto=%s"
    cursor.execute(sql, (nombre, precio, stock, id))
    conn.commit()
    conn.close()

def eliminar_producto(id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id_producto=%s", (id,))
    conn.commit()
    conn.close()
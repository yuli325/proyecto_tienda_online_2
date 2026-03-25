from conexion.conexion import obtener_conexion

def obtener_productos():
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos")
        datos = cursor.fetchall()
        conn.close()
        return datos
    except Exception as e:
        print("Error obtener_productos:", e)
        return []


def obtener_producto(id):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos WHERE id_producto=%s", (id,))
        dato = cursor.fetchone()
        conn.close()
        return dato
    except Exception as e:
        print("Error obtener_producto:", e)
        return None


def crear_producto(nombre, precio, stock):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        sql = "INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nombre, precio, stock))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Error crear_producto:", e)


def actualizar_producto(id, nombre, precio, stock):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        sql = "UPDATE productos SET nombre=%s, precio=%s, stock=%s WHERE id_producto=%s"
        cursor.execute(sql, (nombre, precio, stock, id))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Error actualizar_producto:", e)


def eliminar_producto(id):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id_producto=%s", (id,))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Error eliminar_producto:", e)
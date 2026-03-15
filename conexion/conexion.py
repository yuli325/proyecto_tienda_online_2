import mysql.connector

def obtener_conexion():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="@Lupita2026",
        database="tienda_online"
    )
    return conexion

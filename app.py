from flask import Flask, render_template, request, redirect, url_for
import os

# Funciones de SQLite que ya usabas
from database import (
    crear_tabla,
    obtener_productos,
    insertar_producto,
    actualizar_producto,
    eliminar_producto
)

# Funciones para persistencia en archivos
from archivos import guardar_txt, guardar_json, guardar_csv, leer_txt, leer_json, leer_csv

# Conexión a MySQL
from conexion.conexion import obtener_conexion

app = Flask(__name__)

# =========================
# Crear tabla SQLite al iniciar la app
# =========================
crear_tabla()

# =========================
# Ruta principal: muestra todos los productos (SQLite)
# =========================
@app.route("/")
def home():
    productos = obtener_productos()
    return render_template("index.html", productos=productos)

# =========================
# Ruta dinámica para mostrar un producto
# =========================
@app.route("/producto/<nombre>")
def producto(nombre):
    return render_template(
        "base.html",
        title=f"Producto {nombre}",
        content=f"Producto: {nombre} – disponible"
    )

# =========================
# Página About
# =========================
@app.route("/about")
def about():
    return render_template("about.html")

# =========================
# Página Contacto
# =========================
@app.route("/contactos")
def contactos():
    return render_template("contactos.html")

# =========================
# Agregar producto (SQLite)
# =========================
@app.route("/agregar", methods=["GET", "POST"])
def agregar():

    if request.method == "POST":
        nombre = request.form["nombre"]
        precio = request.form["precio"]
        descripcion = request.form["descripcion"]

        insertar_producto(nombre, precio, descripcion)

        return redirect(url_for("home"))

    return render_template("agregar.html")

# =========================
# Editar producto
# =========================
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    if request.method == "POST":
        nombre = request.form["nombre"]
        precio = request.form["precio"]
        descripcion = request.form["descripcion"]

        actualizar_producto(id, nombre, precio, descripcion)

        return redirect(url_for("home"))

    productos = obtener_productos()
    producto = [p for p in productos if p[0] == id][0]

    return render_template("editar.html", producto=producto)

# =========================
# Eliminar producto
# =========================
@app.route("/eliminar/<int:id>")
def eliminar(id):

    eliminar_producto(id)

    return redirect(url_for("home"))

# =========================
# MOSTRAR PRODUCTOS MYSQL (BONITO)
# =========================
@app.route("/productos_mysql")
def productos_mysql():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    conexion.close()

    return render_template("productos_mysql.html", productos=productos)

# =========================
# Insertar producto en MySQL
# =========================
@app.route("/agregar_mysql", methods=["POST"])
def agregar_mysql():

    nombre = request.form["nombre"]
    precio = request.form["precio"]
    descripcion = request.form["descripcion"]

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    sql = "INSERT INTO productos (nombre, precio, descripcion) VALUES (%s,%s,%s)"
    valores = (nombre, precio, descripcion)

    cursor.execute(sql, valores)
    conexion.commit()

    conexion.close()

    return redirect("/productos_mysql")

# =========================
# Ejecutar aplicación
# =========================
if __name__ == "__main__":
    app.run(debug=True)

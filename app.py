from flask import Flask, render_template, request, redirect, url_for
import os
from database import (
    crear_tabla,
    obtener_productos,
    insertar_producto,
    actualizar_producto,
    eliminar_producto
)

# Funciones para persistencia en archivos
from archivos import guardar_txt, guardar_json, guardar_csv, leer_txt, leer_json, leer_csv

app = Flask(__name__)

# =========================
# Crear tabla SQLite al iniciar la app
# =========================
crear_tabla()

# =========================
# Ruta principal: muestra todos los productos
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
# Página Contactos
# =========================
@app.route("/contactos")
def contactos():
    return render_template("contactos.html")

# =========================
# Ruta para ver productos en archivos (TXT, JSON, CSV)
# =========================
@app.route("/datos")
def datos():
    txt = leer_txt()
    json_datos = leer_json()
    csv_datos = leer_csv()
    return render_template("datos.html", txt=txt, json_datos=json_datos, csv_datos=csv_datos)

# =========================
# Ruta para agregar productos
# =========================
@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    if request.method == "POST":
        nombre = request.form["nombre"]
        cantidad = int(request.form["cantidad"])
        precio = float(request.form["precio"])

        # Guardar en SQLite
        insertar_producto(nombre, cantidad, precio)

        # Guardar también en archivos
        guardar_txt(nombre, cantidad, precio)
        guardar_json(nombre, cantidad, precio)
        guardar_csv(nombre, cantidad, precio)

        return redirect(url_for("home"))

    return render_template(
        "producto_form.html",
        titulo="Agregar Producto",
        boton="Agregar",
        producto=None
    )

# =========================
# Ruta para editar productos
# =========================
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    productos = obtener_productos()
    producto = next((p for p in productos if p[0] == id), None)

    if not producto:
        return "Producto no encontrado"

    if request.method == "POST":
        cantidad = int(request.form["cantidad"])
        precio = float(request.form["precio"])
        actualizar_producto(id, cantidad, precio)
        return redirect(url_for("home"))

    return render_template(
        "producto_form.html",
        titulo=f"Editar Producto: {producto[1]}",
        boton="Guardar Cambios",
        producto={
            "nombre": producto[1],
            "cantidad": producto[2],
            "precio": producto[3]
        }
    )

# =========================
# Ruta para eliminar productos
# =========================
@app.route("/eliminar/<int:id>")
def eliminar(id):
    eliminar_producto(id)
    return redirect(url_for("home"))

# =========================
# Ejecutar la app
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
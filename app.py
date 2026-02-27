from flask import Flask, render_template, request, redirect, url_for
import os
from database import (
    crear_tabla,
    obtener_productos,
    insertar_producto,
    actualizar_producto,
    eliminar_producto
)

app = Flask(__name__)

# =========================================
# Crear tabla productos al iniciar la app
# =========================================
crear_tabla()

# =========================================
# Ruta principal: muestra todos los productos
# =========================================
@app.route("/")
def home():
    productos = obtener_productos()
    return render_template("index.html", productos=productos)

# =========================================
# Ruta dinámica para mostrar un producto
# =========================================
@app.route("/producto/<nombre>")
def producto(nombre):
    return render_template(
        "base.html",
        title=f"Producto {nombre}",
        content=f"Producto: {nombre} – disponible"
    )

# =========================================
# Página About
# =========================================
@app.route("/about")
def about():
    return render_template("about.html")

# =========================================
# Ruta para agregar productos
# =========================================
@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    if request.method == "POST":
        nombre = request.form["nombre"]
        cantidad = int(request.form["cantidad"])
        precio = float(request.form["precio"])
        insertar_producto(nombre, cantidad, precio)
        return redirect(url_for("home"))
    return render_template("agregar.html")

# =========================================
# Ruta para editar productos
# =========================================
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

    return render_template("editar.html", producto=producto)

# =========================================
# Ruta para eliminar productos
# =========================================
@app.route("/eliminar/<int:id>")
def eliminar(id):
    eliminar_producto(id)
    return redirect(url_for("home"))

# =========================================
# Ejecutar la app
# =========================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)  # debug=True para ver errores
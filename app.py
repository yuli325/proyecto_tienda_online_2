from flask import Flask, render_template, request, redirect, url_for
import os

# =========================
# Flask-Login
# =========================
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from usuario_model import Usuario

# 🔐 ENCRIPTACIÓN
from werkzeug.security import generate_password_hash, check_password_hash

# =========================
# Funciones de SQLite
# =========================
from database import (
    crear_tabla,
    obtener_productos,
    insertar_producto,
    actualizar_producto,
    eliminar_producto
)

# =========================
# Funciones de archivos
# =========================
from archivos import guardar_txt, guardar_json, guardar_csv, leer_txt, leer_json, leer_csv

# =========================
# MySQL
# =========================
try:
    from conexion.conexion import obtener_conexion
except:
    obtener_conexion = None

app = Flask(__name__)
app.secret_key = "secreto123"

# =========================
# Flask-Login config
# =========================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# =========================
# Cargar usuario
# =========================
@login_manager.user_loader
def load_user(user_id):
    if not obtener_conexion:
        return None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (user_id,))
        user = cursor.fetchone()

        conexion.close()

        if user:
            return Usuario(user[0], user[1], user[2], user[3])

    except:
        return None

    return None

# =========================
# REGISTRO 🔐
# =========================
@app.route("/registro", methods=["GET", "POST"])
def registro():

    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]

        # 🔐 ENCRIPTAR PASSWORD
        password = generate_password_hash(request.form["password"])

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()

            sql = "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)"
            valores = (nombre, email, password)

            cursor.execute(sql, valores)
            conexion.commit()
            conexion.close()

            return redirect(url_for("login"))

        except Exception as e:
            return f"Error al registrar: {e}"

    return render_template("registro.html")

# =========================
# Crear tabla SQLite
# =========================
crear_tabla()

# =========================
# LOGIN 🔐
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"].strip()

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()

            # 🔥 SOLO BUSCA POR EMAIL
            cursor.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
            user = cursor.fetchone()

            conexion.close()

            # 🔐 VERIFICAR HASH
            if user and check_password_hash(user[3], password):
                usuario = Usuario(user[0], user[1], user[2], user[3])
                login_user(usuario)
                return redirect(url_for("home"))
            else:
                return "Credenciales incorrectas"

        except Exception as e:
            return f"Error de conexión: {e}"

    return render_template("login.html")

# =========================
# LOGOUT
# =========================
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# =========================
# HOME (PROTEGIDA)
# =========================
@app.route("/")
@login_required
def home():
    productos = obtener_productos()
    return render_template("index.html", productos=productos)

# =========================
# PRODUCTO
# =========================
@app.route("/producto/<nombre>")
@login_required
def producto(nombre):
    return render_template(
        "base.html",
        title=f"Producto {nombre}",
        content=f"Producto: {nombre} – disponible"
    )

# =========================
# ABOUT
# =========================
@app.route("/about")
def about():
    return render_template("about.html")

# =========================
# CONTACTOS
# =========================
@app.route("/contactos")
def contactos():
    return render_template("contactos.html")

# =========================
# AGREGAR PRODUCTO
# =========================
@app.route("/agregar", methods=["GET", "POST"])
@login_required
def agregar():

    if request.method == "POST":
        nombre = request.form["nombre"]
        precio = request.form["precio"]
        descripcion = request.form["descripcion"]

        insertar_producto(nombre, precio, descripcion)

        return redirect(url_for("home"))

    return render_template("agregar.html")

# =========================
# EDITAR
# =========================
@app.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
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
# ELIMINAR
# =========================
@app.route("/eliminar/<int:id>")
@login_required
def eliminar(id):

    eliminar_producto(id)

    return redirect(url_for("home"))

# =========================
# MYSQL PRODUCTOS
# =========================
@app.route("/productos_mysql")
@login_required
def productos_mysql():

    if not obtener_conexion:
        return "MySQL no disponible en este servidor"

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()

        conexion.close()

        return render_template("productos_mysql.html", productos=productos)

    except:
        return "Error al conectar con MySQL"

# =========================
# INSERTAR MYSQL
# =========================
@app.route("/agregar_mysql", methods=["POST"])
@login_required
def agregar_mysql():

    if not obtener_conexion:
        return "MySQL no disponible"

    try:
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

    except:
        return "Error al insertar producto en MySQL"

# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
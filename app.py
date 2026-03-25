from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import io

# =========================
# Flask-Login
# =========================
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from usuario_model import Usuario

# 🔐 ENCRIPTACIÓN
from werkzeug.security import generate_password_hash, check_password_hash

# =========================
# SQLite
# =========================
from database import (
    crear_tabla,
    obtener_productos,
    insertar_producto,
    actualizar_producto,
    eliminar_producto
)

# =========================
# MySQL
# =========================
try:
    from conexion.conexion import obtener_conexion
except:
    obtener_conexion = None

# =========================
# SERVICES (MySQL)
# =========================
from services.producto_service import (
    obtener_productos as obtener_productos_mysql_service,
    crear_producto,
    obtener_producto,
    actualizar_producto as actualizar_producto_mysql,
    eliminar_producto as eliminar_producto_mysql
)

# =========================
# PDF
# =========================
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.secret_key = "secreto123"

# =========================
# Flask-Login config
# =========================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# =========================
# USER LOADER (🔥 CORREGIDO)
# =========================
@login_manager.user_loader
def load_user(user_id):
    # 🔥 PROTECCIÓN PARA RENDER
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
# REGISTRO
# =========================
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()

            cursor.execute(
                "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
                (nombre, email, password)
            )

            conexion.commit()
            conexion.close()

            return redirect(url_for("login"))

        except Exception as e:
            return f"Error: {e}"

    return render_template("registro.html")

# =========================
# LOGIN
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()

            cursor.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
            user = cursor.fetchone()

            conexion.close()

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
# HOME
# =========================
crear_tabla()

@app.route("/")
@login_required
def home():
    productos = obtener_productos()
    return render_template("index.html", productos=productos)

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
# PRODUCTO
# =========================
@app.route("/producto/<nombre>")
@login_required
def producto(nombre):
    return f"Producto: {nombre}"

# =========================
# CRUD SQLITE
# =========================
@app.route("/agregar", methods=["GET", "POST"])
@login_required
def agregar():
    if request.method == "POST":
        insertar_producto(
            request.form["nombre"],
            request.form["precio"],
            request.form["descripcion"]
        )
        return redirect(url_for("home"))

    return render_template("agregar.html")

@app.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    if request.method == "POST":
        actualizar_producto(
            id,
            request.form["nombre"],
            request.form["precio"],
            request.form["descripcion"]
        )
        return redirect(url_for("home"))

    productos = obtener_productos()
    producto = [p for p in productos if p[0] == id][0]

    return render_template("editar.html", producto=producto)

@app.route("/eliminar/<int:id>")
@login_required
def eliminar(id):
    eliminar_producto(id)
    return redirect(url_for("home"))

# =========================
# CRUD MYSQL
# =========================
@app.route("/productos")
@login_required
def listar_productos():
    productos = obtener_productos_mysql_service()
    return render_template("productos/listar.html", productos=productos)

# 🔥 REDIRECT PARA MENÚ
@app.route("/productos_mysql")
@login_required
def productos_mysql_redirect():
    return redirect("/productos")

@app.route("/productos/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_producto():
    if request.method == "POST":
        crear_producto(
            request.form["nombre"],
            request.form["precio"],
            request.form["stock"]
        )
        return redirect("/productos")

    return render_template("productos/form.html")

@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_producto_mysql(id):
    producto = obtener_producto(id)

    if request.method == "POST":
        actualizar_producto_mysql(
            id,
            request.form["nombre"],
            request.form["precio"],
            request.form["stock"]
        )
        return redirect("/productos")

    return render_template("productos/form.html", producto=producto)

@app.route("/productos/eliminar/<int:id>")
@login_required
def eliminar_producto_mysql_route(id):
    eliminar_producto_mysql(id)
    return redirect("/productos")

# =========================
# PDF
# =========================
@app.route("/reporte_pdf")
@login_required
def reporte_pdf():
    productos = obtener_productos_mysql_service()

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    y = 750
    pdf.drawString(200, 800, "REPORTE DE PRODUCTOS")

    for p in productos:
        texto = f"ID:{p[0]} | {p[1]} | Precio:{p[2]} | Stock:{p[3]}"
        pdf.drawString(50, y, texto)
        y -= 20

    pdf.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="reporte.pdf", mimetype="application/pdf")

# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
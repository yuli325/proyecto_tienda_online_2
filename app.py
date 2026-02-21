from flask import Flask, render_template
import os

app = Flask(__name__)

# Ruta principal
@app.route("/")
def home():
    return render_template("index.html")

# Ruta dinámica para productos
@app.route("/producto/<nombre>")
def producto(nombre):
    return render_template("base.html", title=f"Producto {nombre}", content=f"Producto: {nombre} – disponible")

# Página "Acerca de"
@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
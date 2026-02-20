from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Bienvenido a Tienda Online – Catálogo y ofertas"

@app.route("/producto/<nombre>")
def producto(nombre):
    return f"Producto: {nombre} – disponible"

if __name__ == "__main__":
    # Para producción en Render:
    port = int(os.environ.get("PORT", 5000))  # Usa el puerto de Render o 5000 local
    app.run(host="0.0.0.0", port=port)
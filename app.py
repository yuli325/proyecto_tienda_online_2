from flask import Flask

app = Flask(__name__)

@app.route('/')
def inicio():
    return "Bienvenido a Tienda Online – Catálogo y Ofertas"

@app.route('/producto/<nombre>')
def producto(nombre):
    return f"Producto: {nombre} – disponible en nuestra tienda online."

if __name__ == '__main__':
    app.run(debug=True)
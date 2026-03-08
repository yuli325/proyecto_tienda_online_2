import os
import json
import csv

# Carpeta donde guardamos los archivos
DATA_DIR = os.path.join("inventario", "data")

# Archivos de datos
TXT_FILE = os.path.join(DATA_DIR, "datos.txt")
JSON_FILE = os.path.join(DATA_DIR, "datos.json")
CSV_FILE = os.path.join(DATA_DIR, "datos.csv")

# =========================
# Crear carpeta y archivos si no existen
# =========================
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Crear archivo TXT si no existe
if not os.path.exists(TXT_FILE):
    open(TXT_FILE, "w", encoding="utf-8").close()

# Crear archivo JSON si no existe
if not os.path.exists(JSON_FILE):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

# Crear archivo CSV si no existe
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["nombre", "cantidad", "precio"])

# =========================
# Funciones para guardar
# =========================
def guardar_txt(nombre, cantidad, precio):
    with open(TXT_FILE, "a", encoding="utf-8") as f:
        f.write(f"{nombre},{cantidad},{precio}\n")

def guardar_json(nombre, cantidad, precio):
    datos = leer_json()
    datos.append({"nombre": nombre, "cantidad": cantidad, "precio": precio})
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

def guardar_csv(nombre, cantidad, precio):
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([nombre, cantidad, precio])

# =========================
# Funciones para leer
# =========================
def leer_txt():
    productos = []
    if os.path.exists(TXT_FILE):
        with open(TXT_FILE, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if linea:
                    nombre, cantidad, precio = linea.split(",")
                    productos.append({"nombre": nombre, "cantidad": int(cantidad), "precio": float(precio)})
    return productos

def leer_json():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            try:
                datos = json.load(f)
                return datos
            except json.JSONDecodeError:
                return []
    return []

def leer_csv():
    productos = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                productos.append({"nombre": row["nombre"], "cantidad": int(row["cantidad"]), "precio": float(row["precio"])})
    return productos
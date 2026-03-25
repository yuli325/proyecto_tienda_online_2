CREATE DATABASE tienda_online;
USE tienda_online;

-- =========================
-- TABLA USUARIOS
-- =========================
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255)
);

-- =========================
-- TABLA PRODUCTOS
-- =========================
CREATE TABLE productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    precio DECIMAL(10,2),
    stock INT
);

-- =========================
-- TABLA CLIENTES
-- =========================
CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100)
);

-- =========================
-- TABLA FACTURAS (RELACIÓN)
-- =========================
CREATE TABLE facturas (
    id_factura INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT,
    fecha DATE,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

-- =========================
-- TABLA DETALLE FACTURA
-- =========================
CREATE TABLE detalle_factura (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_factura INT,
    id_producto INT,
    cantidad INT,
    FOREIGN KEY (id_factura) REFERENCES facturas(id_factura),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);
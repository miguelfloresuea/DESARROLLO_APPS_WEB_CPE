-- Tabla de productos: los planes de internet que ofrece JLM Connect 360
CREATE TABLE IF NOT EXISTS productos (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    velocidad VARCHAR(50) NOT NULL,
    precio VARCHAR(20) NOT NULL,
    descripcion TEXT NOT NULL
);

-- Tabla de proveedores: empresas que suministran equipos de red
CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    producto VARCHAR(150) NOT NULL,
    contacto VARCHAR(100) NOT NULL
);

-- Tabla de clientes: quienes contratan un plan
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    sector VARCHAR(100) NOT NULL,
    plan VARCHAR(50) NOT NULL,
    estado VARCHAR(50) NOT NULL
);

-- Tabla de facturas: cada factura pertenece a un cliente (clave foranea id_cliente)
CREATE TABLE IF NOT EXISTS facturas (
    id_factura SERIAL PRIMARY KEY,
    numero VARCHAR(20) NOT NULL,
    id_cliente INTEGER NOT NULL,
    monto VARCHAR(20) NOT NULL,
    estado VARCHAR(50) NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

-- Datos iniciales de los 4 planes que ya manejaba el proyecto
INSERT INTO productos (nombre, velocidad, precio, descripcion) VALUES
('Plan Residencial', '20 Mbps', '$18.00', 'Ideal para navegación, streaming y videollamadas familiares.'),
('Plan Empresarial', '50 Mbps simétrico', '$45.00', 'Conexión de alta velocidad y estabilidad para negocios.'),
('Plan Educativo', '15 Mbps', '$12.00', 'Tarifa preferencial para instituciones educativas.'),
('Plan Rural', '10 Mbps', '$15.00', 'Cobertura mediante enlaces punto a multipunto de 5 GHz.');

-- Datos iniciales de proveedores
INSERT INTO proveedores (nombre, producto, contacto) VALUES
('TP-Link Ecuador', 'Routers y repetidores', 'ventas@tplink.ec'),
('Ubiquiti Networks', 'Equipos punto a multipunto 5 GHz', 'soporte@ubnt.com'),
('Fibercorp', 'Cable de fibra óptica y accesorios', 'contacto@fibercorp.ec');

-- Datos iniciales de clientes
INSERT INTO clientes (nombre, sector, plan, estado) VALUES
('Carlos Andrade', 'Macas Centro', 'Residencial', 'Activo'),
('Distribuidora Amazónica', 'Zona Industrial', 'Empresarial', 'Activo'),
('Unidad Educativa Emanuel', 'Macas Centro', 'Educativo', 'Activo'),
('Familia Chumpi', 'Sinaí', 'Rural', 'Pendiente instalación');

-- Facturas de ejemplo, cada una ligada a un cliente por id_cliente
INSERT INTO facturas (numero, id_cliente, monto, estado) VALUES
('F001-000123', 1, '$18.00', 'Pagada'),
('F001-000124', 2, '$45.00', 'Pendiente'),
('F001-000125', 3, '$12.00', 'Pagada');

-- ===================== SISTEMA DE LOGIN  =====================

-- Tabla de usuarios: cuentas para iniciar sesión en el sistema
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- ===================== RELACIONES ADICIONALES (núcleo: facturas) =====================

-- Cada producto pertenece a un proveedor
ALTER TABLE productos
ADD COLUMN IF NOT EXISTS id_proveedor INTEGER REFERENCES proveedores(id_proveedor);

-- Cada factura fue registrada por un usuario del sistema
ALTER TABLE facturas
ADD COLUMN IF NOT EXISTS id_usuario INTEGER REFERENCES usuarios(id);

-- Detalle de cada factura: qué productos incluye
CREATE TABLE IF NOT EXISTS detalle_factura (
    id_detalle SERIAL PRIMARY KEY,
    id_factura INTEGER REFERENCES facturas(id_factura),
    id_producto INTEGER REFERENCES productos(id_producto),
    cantidad INTEGER NOT NULL,
    precio_unitario NUMERIC(10,2) NOT NULL,
    subtotal NUMERIC(10,2) NOT NULL
);
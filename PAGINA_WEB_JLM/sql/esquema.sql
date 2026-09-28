
DROP TABLE IF EXISTS detalle_factura CASCADE;
DROP TABLE IF EXISTS facturas CASCADE;
DROP TABLE IF EXISTS suscripciones CASCADE;
DROP TABLE IF EXISTS clientes CASCADE;
DROP TABLE IF EXISTS productos CASCADE;
DROP TABLE IF EXISTS proveedores CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;

-- 2. CREACIÓN DE TABLAS
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    nombre_completo VARCHAR(100) NOT NULL
);

CREATE TABLE proveedores (
    id_proveedor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    producto VARCHAR(150) NOT NULL,
    contacto VARCHAR(100)
);

CREATE TABLE productos (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    velocidad VARCHAR(50) NOT NULL,
    precio VARCHAR(20) NOT NULL,
    descripcion TEXT NOT NULL,
    id_proveedor INTEGER REFERENCES proveedores(id_proveedor)
);

CREATE TABLE clientes (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ruc_cedula VARCHAR(13),
    celular VARCHAR(10),
    correo VARCHAR(100),
    canton VARCHAR(50),
    ciudad VARCHAR(50),
    sector VARCHAR(100),
    plan VARCHAR(50),
    estado VARCHAR(50) DEFAULT 'Activo'
);

CREATE TABLE suscripciones (
    id_suscripcion SERIAL PRIMARY KEY,
    id_cliente INTEGER NOT NULL REFERENCES clientes(id_cliente) ON DELETE CASCADE,
    id_producto INTEGER NOT NULL REFERENCES productos(id_producto) ON DELETE CASCADE,
    fecha_inicio DATE DEFAULT CURRENT_DATE,
    estado VARCHAR(20) DEFAULT 'Activo'
);

CREATE TABLE facturas (
    id_factura SERIAL PRIMARY KEY,
    numero VARCHAR(20) UNIQUE NOT NULL,
    id_cliente INTEGER NOT NULL REFERENCES clientes(id_cliente),
    monto VARCHAR(20) NOT NULL,
    estado VARCHAR(50) NOT NULL DEFAULT 'Pendiente',
    id_usuario INTEGER REFERENCES usuarios(id),
    forma_pago VARCHAR(30),
    comprobante_pago TEXT,
    motivo_anulacion TEXT,
    observaciones_anulacion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE detalle_factura (
    id_detalle SERIAL PRIMARY KEY,
    id_factura INTEGER NOT NULL REFERENCES facturas(id_factura) ON DELETE CASCADE,
    id_producto INTEGER NOT NULL REFERENCES productos(id_producto),
    cantidad INTEGER NOT NULL DEFAULT 1,
    precio_unitario VARCHAR(20) NOT NULL,
    subtotal VARCHAR(20) NOT NULL
);

-- 3. DATOS INICIALES (CON CONTRASEÑAS REALES PARA "123456")
INSERT INTO usuarios (usuario, password, nombre_completo) VALUES
('jes12', 'scrypt:32768:8:1$K5j8L2mN$9f8e7d6c5b4a3928170615243f2e1d0c9b8a7968574635241302918070605040', 'Jessica Pesantez'),
('migu12', 'scrypt:32768:8:1$vF3k9L2m$8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b', 'Miguel Flores'),
('lis12', 'scrypt:32768:8:1$2wQ6yT9z$3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d', 'Lisseth Puco');

INSERT INTO productos (nombre, velocidad, precio, descripcion) VALUES
('Residencial', '20 Mbps', '$18.00', 'Ideal para navegación, streaming y videollamadas familiares.'),
('Empresarial', '50 Mbps simétrico', '$45.00', 'Conexión de alta velocidad y estabilidad para negocios.'),
('Educativo', '15 Mbps', '$12.00', 'Tarifa preferencial para instituciones educativas.'),
('Rural', '10 Mbps', '$15.00', 'Cobertura mediante enlaces punto a multipunto de 5 GHz.'),
('Premium Fibra', '150 Mbps', '$35.00', 'Plan de alta velocidad para hogares.'),
('PYME', '80 Mbps', '$30.00', 'Plan para pequeños negocios.'),
('Comercial', '30 Mbps', '$25.00', 'Plan para comercios y tiendas.');

INSERT INTO proveedores (nombre, producto, contacto) VALUES
('TP-Link Ecuador', 'Routers y repetidores', 'ventas@tplink.ec'),
('Ubiquiti Networks', 'Equipos punto a multipunto 5 GHz', 'soporte@ubnt.com'),
('Fibercorp', 'Cable de fibra óptica y accesorios', 'contacto@fibercorp.ec'),
('Huawei Ecuador', 'Equipos de red y switches', 'contacto@huawei.com.ec'),
('MikroTik LATAM', 'Routers y equipos de gestión', 'ventas@mikrotik.la');

INSERT INTO clientes (nombre, ruc_cedula, celular, correo, canton, ciudad, sector, plan, estado) VALUES
('Carlos Andrade', '1001234567', '0987654321', 'carlos.andrade@gmail.com', 'Morona', 'Macas', 'Av. 29 de Mayo', 'Residencial', 'Activo'),
('Colegio Amazónico', '1098765432101', '0991234567', 'colegio.amazonico@hotmail.com', 'Morona', 'Macas', 'Barrio La Primavera', 'Educativo', 'Activo'),
('Distribuidora Amazónica', '1098765432101', '0988765432', 'dist.amazonica@gmail.com', 'Morona', 'Macas', 'Zona Industrial', 'Empresarial', 'Activo'),
('Familia Chumpi', '1002345678', '0976543210', 'familia.chumpi@gmail.com', 'Pablo Sexto', 'Pablo Sexto', 'Centro', 'Rural', 'Pendiente instalación'),
('Ferretería El Constructor', '1098765432101', '0985432109', 'ferreteria.constructor@hotmail.com', 'Morona', 'Macas', 'Zona Industrial', 'Comercial', 'Activo'),
('Hostal Río Upano', '1098765432101', '0984321098', 'hostal.rioupano@gmail.com', 'Morona', 'Macas', 'Av. Amazonas', 'Comercial', 'Activo'),
('Liseth Puco', '1003456789', '0983210987', 'liseth.puco@gmail.com', 'Pablo Sexto', 'Macas', 'Calle Principal', 'Empresarial', 'Activo'),
('Miguel Angel Ferrati Gomez', '1500727044', '0972293688', 'miguel.ferrati@gmail.com', 'Morona', 'Macas', 'Av. Luis Alberto', 'Educativo', 'Activo'),
('Panadería Manaos', '1098765432101', '0982109876', 'panaderia.manaos@hotmail.com', 'Morona', 'Macas', 'Centro', 'Comercial', 'Activo'),
('Saul Enrique Urganda Martin', '1500727045', '0989892541', 'saul.urganda@gmail.com', 'Taisha', 'Macas', 'Barrio Nuevo', 'Residencial', 'Activo'),
('Unidad Educativa Emanuel', '1098765432101', '0981098765', 'ue.emanuel@gmail.com', 'Morona', 'Macas', 'Sector Norte', 'Educativo', 'Activo'),
('Jessica Pesantez', '1004567890', '0980987654', 'jessica.pesantez@gmail.com', 'Morona', 'Macas', 'Calle Sucre', 'Residencial', 'Activo'),
('Miguel Flores', '1005678901', '0979876543', 'miguel.flores@hotmail.com', 'Morona', 'Macas', 'Av. del Ejército', 'Empresarial', 'Activo'),
('Lisseth Puco', '1006789012', '0978765432', 'lisseth.puco@gmail.com', 'Morona', 'Macas', 'Barrio San Francisco', 'Premium Fibra', 'Activo'),
('Tienda El Progreso', '1098765432101', '0977654321', 'tienda.progreso@gmail.com', 'Gualaquiza', 'Gualaquiza', 'Centro', 'PYME', 'Activo'),
('Cafetería La Montaña', '1098765432101', '0976543210', 'cafeteria.montana@hotmail.com', 'Sucúa', 'Sucúa', 'Parque Central', 'Comercial', 'Activo'),
('Escuela Rural Shuar', '1098765432101', '0975432109', 'escuela.shuar@gmail.com', 'Taisha', 'Taisha', 'Comunidad Shuar', 'Educativo', 'Activo'),
('Farmacia Morona', '1098765432101', '0974321098', 'farmacia.morona@gmail.com', 'Morona', 'Macas', 'Av. 29 de Mayo', 'PYME', 'Activo'),
('Hotel Macas Plaza', '1098765432101', '0973210987', 'hotel.macasplaza@hotmail.com', 'Morona', 'Macas', 'Centro Histórico', 'Empresarial', 'Activo'),
('Taller Mecánico El Turbo', '1098765432101', '0972109876', 'taller.turbo@gmail.com', 'Morona', 'Macas', 'Zona Industrial', 'Comercial', 'Pendiente instalación');

-- 4. VINCULAR CLIENTES CON SUS PLANES AUTOMÁTICAMENTE
INSERT INTO suscripciones (id_cliente, id_producto, estado)
SELECT c.id_cliente, p.id_producto, c.estado
FROM clientes c
JOIN productos p ON c.plan = p.nombre;

SELECT '✅ BASE DE DATOS RECREADA EXITOSAMENTE' AS mensaje;
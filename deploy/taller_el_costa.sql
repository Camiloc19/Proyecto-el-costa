-- Dump de taller_el_costa generado para despliegue AWS
SET FOREIGN_KEY_CHECKS=0;
SET NAMES utf8mb4;

DROP TABLE IF EXISTS `atencion_vehiculo`;
CREATE TABLE `atencion_vehiculo` (
  `idAtencion` int(11) NOT NULL AUTO_INCREMENT,
  `id_Vehiculo_fk` int(11) NOT NULL,
  `id_Usuario_fk` int(11) NOT NULL,
  `id_Rol_fk` int(11) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_final` date DEFAULT NULL,
  PRIMARY KEY (`idAtencion`),
  KEY `fk_atencion_vehiculo` (`id_Vehiculo_fk`),
  KEY `fk_atencion_usuario` (`id_Usuario_fk`),
  KEY `fk_atencion_rol` (`id_Rol_fk`),
  CONSTRAINT `fk_atencion_rol` FOREIGN KEY (`id_Rol_fk`) REFERENCES `roles` (`idRol`),
  CONSTRAINT `fk_atencion_usuario` FOREIGN KEY (`id_Usuario_fk`) REFERENCES `usuarios` (`idUsuario`),
  CONSTRAINT `fk_atencion_vehiculo` FOREIGN KEY (`id_Vehiculo_fk`) REFERENCES `vehiculos` (`IDvehiculos`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `atencion_vehiculo` (`idAtencion`, `id_Vehiculo_fk`, `id_Usuario_fk`, `id_Rol_fk`, `fecha_inicio`, `fecha_final`) VALUES (1, 1, 2, 4, '2026-03-23', '2026-03-25');
INSERT INTO `atencion_vehiculo` (`idAtencion`, `id_Vehiculo_fk`, `id_Usuario_fk`, `id_Rol_fk`, `fecha_inicio`, `fecha_final`) VALUES (2, 2, 3, 4, '2026-02-18', '2026-03-24');
INSERT INTO `atencion_vehiculo` (`idAtencion`, `id_Vehiculo_fk`, `id_Usuario_fk`, `id_Rol_fk`, `fecha_inicio`, `fecha_final`) VALUES (3, 3, 2, 4, '2026-01-04', '2026-01-06');
INSERT INTO `atencion_vehiculo` (`idAtencion`, `id_Vehiculo_fk`, `id_Usuario_fk`, `id_Rol_fk`, `fecha_inicio`, `fecha_final`) VALUES (4, 4, 3, 4, '2026-01-15', '2026-01-17');
INSERT INTO `atencion_vehiculo` (`idAtencion`, `id_Vehiculo_fk`, `id_Usuario_fk`, `id_Rol_fk`, `fecha_inicio`, `fecha_final`) VALUES (5, 5, 4, 4, '2026-01-30', '2026-02-05');
INSERT INTO `atencion_vehiculo` (`idAtencion`, `id_Vehiculo_fk`, `id_Usuario_fk`, `id_Rol_fk`, `fecha_inicio`, `fecha_final`) VALUES (6, 6, 5, 4, '2026-06-17', NULL);

DROP TABLE IF EXISTS `categoria_producto`;
CREATE TABLE `categoria_producto` (
  `idCategoria` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`idCategoria`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `categoria_producto` (`idCategoria`, `nombre`, `descripcion`) VALUES (1, 'Filtros', 'Retiene impurezas en los sistemas del vehiculo');
INSERT INTO `categoria_producto` (`idCategoria`, `nombre`, `descripcion`) VALUES (2, 'Lujos', 'Mejoran la funcionalidad, comodidad y estetica del vehiculo');
INSERT INTO `categoria_producto` (`idCategoria`, `nombre`, `descripcion`) VALUES (3, 'Repuestos', 'Piezas para remplazar componentes dañados o gastados');
INSERT INTO `categoria_producto` (`idCategoria`, `nombre`, `descripcion`) VALUES (4, 'Llantas', 'Componentes de caucho para el trayecto y frenado');
INSERT INTO `categoria_producto` (`idCategoria`, `nombre`, `descripcion`) VALUES (5, 'Aceites', 'Lubricantes para proteger los componentes mecanicos');

DROP TABLE IF EXISTS `detalle_movimiento`;
CREATE TABLE `detalle_movimiento` (
  `idMovimiento` int(11) NOT NULL AUTO_INCREMENT,
  `id_TipoMovimiento_fk` int(11) NOT NULL,
  `id_Factura_fk` int(11) NOT NULL,
  `id_ProductoProveedor_fk` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  PRIMARY KEY (`idMovimiento`),
  KEY `fk_detmov_tipo` (`id_TipoMovimiento_fk`),
  KEY `fk_detmov_factura` (`id_Factura_fk`),
  KEY `fk_detmov_prodprov` (`id_ProductoProveedor_fk`),
  CONSTRAINT `fk_detmov_factura` FOREIGN KEY (`id_Factura_fk`) REFERENCES `factura` (`idFactura`),
  CONSTRAINT `fk_detmov_prodprov` FOREIGN KEY (`id_ProductoProveedor_fk`) REFERENCES `producto_proveedor` (`idProductoProveedor`),
  CONSTRAINT `fk_detmov_tipo` FOREIGN KEY (`id_TipoMovimiento_fk`) REFERENCES `tipo_movimiento` (`idTipoMovimiento`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `detalle_movimiento` (`idMovimiento`, `id_TipoMovimiento_fk`, `id_Factura_fk`, `id_ProductoProveedor_fk`, `cantidad`) VALUES (1, 2, 1, 1, 1);
INSERT INTO `detalle_movimiento` (`idMovimiento`, `id_TipoMovimiento_fk`, `id_Factura_fk`, `id_ProductoProveedor_fk`, `cantidad`) VALUES (2, 2, 2, 4, 1);

DROP TABLE IF EXISTS `detalle_orden`;
CREATE TABLE `detalle_orden` (
  `idDetalleServicio` int(11) NOT NULL AUTO_INCREMENT,
  `id_Orden_fk` int(11) NOT NULL,
  `id_TipoServicio_fk` int(11) NOT NULL,
  `id_Producto_fk` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  PRIMARY KEY (`idDetalleServicio`),
  KEY `fk_detalle_orden` (`id_Orden_fk`),
  KEY `fk_detalle_tiposervicio` (`id_TipoServicio_fk`),
  KEY `fk_detalle_producto` (`id_Producto_fk`),
  CONSTRAINT `fk_detalle_orden` FOREIGN KEY (`id_Orden_fk`) REFERENCES `orden_servicio` (`Id_orden`),
  CONSTRAINT `fk_detalle_producto` FOREIGN KEY (`id_Producto_fk`) REFERENCES `producto` (`idProducto`),
  CONSTRAINT `fk_detalle_tiposervicio` FOREIGN KEY (`id_TipoServicio_fk`) REFERENCES `tipo_servicio` (`idTipoServicio`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `detalle_orden` (`idDetalleServicio`, `id_Orden_fk`, `id_TipoServicio_fk`, `id_Producto_fk`, `cantidad`, `precio_unitario`) VALUES (1, 1, 1, 1, 1, '45000.00');
INSERT INTO `detalle_orden` (`idDetalleServicio`, `id_Orden_fk`, `id_TipoServicio_fk`, `id_Producto_fk`, `cantidad`, `precio_unitario`) VALUES (2, 2, 2, 2, 2, '30000.00');
INSERT INTO `detalle_orden` (`idDetalleServicio`, `id_Orden_fk`, `id_TipoServicio_fk`, `id_Producto_fk`, `cantidad`, `precio_unitario`) VALUES (3, 3, 2, 3, 3, '140000.00');
INSERT INTO `detalle_orden` (`idDetalleServicio`, `id_Orden_fk`, `id_TipoServicio_fk`, `id_Producto_fk`, `cantidad`, `precio_unitario`) VALUES (4, 4, 1, 4, 1, '30000.00');
INSERT INTO `detalle_orden` (`idDetalleServicio`, `id_Orden_fk`, `id_TipoServicio_fk`, `id_Producto_fk`, `cantidad`, `precio_unitario`) VALUES (5, 5, 1, 5, 2, '220000.00');

DROP TABLE IF EXISTS `estado_orden`;
CREATE TABLE `estado_orden` (
  `idEstado` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`idEstado`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `estado_orden` (`idEstado`, `nombre`) VALUES (1, 'En proceso');
INSERT INTO `estado_orden` (`idEstado`, `nombre`) VALUES (2, 'Finalizado');

DROP TABLE IF EXISTS `factura`;
CREATE TABLE `factura` (
  `idFactura` int(11) NOT NULL AUTO_INCREMENT,
  `id_Orden_fk` int(11) NOT NULL,
  `id_MetodoPago_fk` int(11) NOT NULL,
  `numero_factura` varchar(20) NOT NULL,
  `fecha` date NOT NULL,
  `total` decimal(12,2) NOT NULL,
  PRIMARY KEY (`idFactura`),
  KEY `fk_factura_orden` (`id_Orden_fk`),
  KEY `fk_factura_metodo` (`id_MetodoPago_fk`),
  CONSTRAINT `fk_factura_metodo` FOREIGN KEY (`id_MetodoPago_fk`) REFERENCES `metodo_pago` (`idMetodoPago`),
  CONSTRAINT `fk_factura_orden` FOREIGN KEY (`id_Orden_fk`) REFERENCES `orden_servicio` (`Id_orden`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `factura` (`idFactura`, `id_Orden_fk`, `id_MetodoPago_fk`, `numero_factura`, `fecha`, `total`) VALUES (1, 1, 1, '1001', '2026-03-04', '250000.00');
INSERT INTO `factura` (`idFactura`, `id_Orden_fk`, `id_MetodoPago_fk`, `numero_factura`, `fecha`, `total`) VALUES (2, 2, 2, '1002', '2026-03-04', '180000.00');

DROP TABLE IF EXISTS `marca_vehiculo`;
CREATE TABLE `marca_vehiculo` (
  `idMarca` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`idMarca`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (1, 'Chevrolet');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (2, 'Mazda');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (3, 'Renault');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (4, 'Toyota');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (5, 'Nissan');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (6, 'Kia');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (7, 'Hyundai');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (8, 'Ford');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (9, 'Volkswagen');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (10, 'Honda');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (11, 'Suzuki');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (12, 'Mitsubishi');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (13, 'Jeep');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (14, 'BMW');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (15, 'Mercedes-Benz');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (16, 'Audi');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (17, 'Peugeot');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (18, 'Citroen');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (19, 'Fiat');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (20, 'Subaru');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (21, 'Volvo');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (22, 'Land Rover');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (23, 'Dodge');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (24, 'RAM');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (25, 'Chery');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (26, 'JAC');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (27, 'Great Wall');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (28, 'BYD');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (29, 'Mini');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (30, 'Porsche');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (31, 'Lexus');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (32, 'Acura');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (33, 'Changan');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (34, 'Foton');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (35, 'SsangYong');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (36, 'Skoda');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (37, 'SEAT');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (38, 'Tesla');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (39, 'Jetour');
INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES (40, 'MG');

DROP TABLE IF EXISTS `metodo_pago`;
CREATE TABLE `metodo_pago` (
  `idMetodoPago` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`idMetodoPago`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `metodo_pago` (`idMetodoPago`, `nombre`) VALUES (1, 'Efectivo');
INSERT INTO `metodo_pago` (`idMetodoPago`, `nombre`) VALUES (2, 'Nequi');

DROP TABLE IF EXISTS `orden_servicio`;
CREATE TABLE `orden_servicio` (
  `Id_orden` int(11) NOT NULL AUTO_INCREMENT,
  `id_Vehiculo_fk` int(11) NOT NULL,
  `id_Usuario_fk` int(11) NOT NULL,
  `id_Estado_fk` int(11) NOT NULL,
  `numero_orden` varchar(50) NOT NULL,
  `hora_apertura` varchar(20) DEFAULT NULL,
  `fecha_apertura` date NOT NULL,
  `fecha_cierre` date DEFAULT NULL,
  `total` decimal(12,2) DEFAULT NULL,
  PRIMARY KEY (`Id_orden`),
  KEY `fk_orden_vehiculo` (`id_Vehiculo_fk`),
  KEY `fk_orden_usuario` (`id_Usuario_fk`),
  KEY `fk_orden_estado` (`id_Estado_fk`),
  CONSTRAINT `fk_orden_estado` FOREIGN KEY (`id_Estado_fk`) REFERENCES `estado_orden` (`idEstado`),
  CONSTRAINT `fk_orden_usuario` FOREIGN KEY (`id_Usuario_fk`) REFERENCES `usuarios` (`idUsuario`),
  CONSTRAINT `fk_orden_vehiculo` FOREIGN KEY (`id_Vehiculo_fk`) REFERENCES `vehiculos` (`IDvehiculos`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `orden_servicio` (`Id_orden`, `id_Vehiculo_fk`, `id_Usuario_fk`, `id_Estado_fk`, `numero_orden`, `hora_apertura`, `fecha_apertura`, `fecha_cierre`, `total`) VALUES (1, 1, 6, 1, '5001', '08:00 AM', '2026-03-02', '2026-03-04', '250000.00');
INSERT INTO `orden_servicio` (`Id_orden`, `id_Vehiculo_fk`, `id_Usuario_fk`, `id_Estado_fk`, `numero_orden`, `hora_apertura`, `fecha_apertura`, `fecha_cierre`, `total`) VALUES (2, 2, 7, 1, '5002', '09:30 AM', '2026-03-13', '2026-03-15', '180000.00');
INSERT INTO `orden_servicio` (`Id_orden`, `id_Vehiculo_fk`, `id_Usuario_fk`, `id_Estado_fk`, `numero_orden`, `hora_apertura`, `fecha_apertura`, `fecha_cierre`, `total`) VALUES (3, 3, 8, 2, '5003', '10:15 AM', '2026-03-04', '2026-06-17', '150.00');
INSERT INTO `orden_servicio` (`Id_orden`, `id_Vehiculo_fk`, `id_Usuario_fk`, `id_Estado_fk`, `numero_orden`, `hora_apertura`, `fecha_apertura`, `fecha_cierre`, `total`) VALUES (4, 4, 9, 1, '5004', '12:00 PM', '2026-03-15', '2026-03-17', NULL);
INSERT INTO `orden_servicio` (`Id_orden`, `id_Vehiculo_fk`, `id_Usuario_fk`, `id_Estado_fk`, `numero_orden`, `hora_apertura`, `fecha_apertura`, `fecha_cierre`, `total`) VALUES (5, 5, 10, 2, '5005', '02:22 PM', '2026-03-17', '2026-03-19', NULL);
INSERT INTO `orden_servicio` (`Id_orden`, `id_Vehiculo_fk`, `id_Usuario_fk`, `id_Estado_fk`, `numero_orden`, `hora_apertura`, `fecha_apertura`, `fecha_cierre`, `total`) VALUES (6, 1, 2, 1, '6001', '08:00 AM', '2026-06-02', NULL, NULL);
INSERT INTO `orden_servicio` (`Id_orden`, `id_Vehiculo_fk`, `id_Usuario_fk`, `id_Estado_fk`, `numero_orden`, `hora_apertura`, `fecha_apertura`, `fecha_cierre`, `total`) VALUES (7, 2, 3, 1, '6002', '09:00 AM', '2026-06-02', NULL, NULL);
INSERT INTO `orden_servicio` (`Id_orden`, `id_Vehiculo_fk`, `id_Usuario_fk`, `id_Estado_fk`, `numero_orden`, `hora_apertura`, `fecha_apertura`, `fecha_cierre`, `total`) VALUES (8, 3, 2, 1, '6003', '10:00 AM', '2026-06-02', NULL, NULL);
INSERT INTO `orden_servicio` (`Id_orden`, `id_Vehiculo_fk`, `id_Usuario_fk`, `id_Estado_fk`, `numero_orden`, `hora_apertura`, `fecha_apertura`, `fecha_cierre`, `total`) VALUES (15, 1, 10, 1, '6004', '18:22', '2026-06-17', NULL, NULL);
INSERT INTO `orden_servicio` (`Id_orden`, `id_Vehiculo_fk`, `id_Usuario_fk`, `id_Estado_fk`, `numero_orden`, `hora_apertura`, `fecha_apertura`, `fecha_cierre`, `total`) VALUES (16, 2, 8, 1, '6005', '06:25', '2027-06-19', NULL, NULL);
INSERT INTO `orden_servicio` (`Id_orden`, `id_Vehiculo_fk`, `id_Usuario_fk`, `id_Estado_fk`, `numero_orden`, `hora_apertura`, `fecha_apertura`, `fecha_cierre`, `total`) VALUES (17, 2, 2, 1, '6006', '18:58', '2026-06-17', NULL, NULL);
INSERT INTO `orden_servicio` (`Id_orden`, `id_Vehiculo_fk`, `id_Usuario_fk`, `id_Estado_fk`, `numero_orden`, `hora_apertura`, `fecha_apertura`, `fecha_cierre`, `total`) VALUES (18, 6, 12, 1, '6007', '21:10', '2026-06-17', NULL, NULL);

DROP TABLE IF EXISTS `producto`;
CREATE TABLE `producto` (
  `idProducto` int(11) NOT NULL AUTO_INCREMENT,
  `id_Categoria_fk` int(11) NOT NULL,
  `nombre_producto` varchar(150) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `stock` int(11) NOT NULL DEFAULT 0,
  `stock_minimo` int(11) NOT NULL DEFAULT 0,
  `precio_compra` decimal(10,2) NOT NULL,
  `precio_venta` decimal(10,2) NOT NULL,
  PRIMARY KEY (`idProducto`),
  KEY `fk_producto_categoria` (`id_Categoria_fk`),
  CONSTRAINT `fk_producto_categoria` FOREIGN KEY (`id_Categoria_fk`) REFERENCES `categoria_producto` (`idCategoria`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `producto` (`idProducto`, `id_Categoria_fk`, `nombre_producto`, `descripcion`, `stock`, `stock_minimo`, `precio_compra`, `precio_venta`) VALUES (1, 5, 'Filtro de aceite', 'Filtro para motor 1.6L - 2.0L', 25, 10, '45000.00', '70000.00');
INSERT INTO `producto` (`idProducto`, `id_Categoria_fk`, `nombre_producto`, `descripcion`, `stock`, `stock_minimo`, `precio_compra`, `precio_venta`) VALUES (2, 2, 'Pastillas de freno', 'Juego delantero para automóvil sedan', 18, 18, '120000.00', '180000.00');
INSERT INTO `producto` (`idProducto`, `id_Categoria_fk`, `nombre_producto`, `descripcion`, `stock`, `stock_minimo`, `precio_compra`, `precio_venta`) VALUES (3, 3, 'Batería 12V 60Ah', 'Batería automotriz libre mantenimiento', 12, 5, '280000.00', '360000.00');
INSERT INTO `producto` (`idProducto`, `id_Categoria_fk`, `nombre_producto`, `descripcion`, `stock`, `stock_minimo`, `precio_compra`, `precio_venta`) VALUES (4, 5, 'Aceite 10W-40', 'Aceite sintético para motor - 1 litro', 40, 15, '30000.00', '45000.00');
INSERT INTO `producto` (`idProducto`, `id_Categoria_fk`, `nombre_producto`, `descripcion`, `stock`, `stock_minimo`, `precio_compra`, `precio_venta`) VALUES (5, 3, 'Bujía estándar', 'Bujía para motor gasolina', 50, 20, '12000.00', '20000.00');
INSERT INTO `producto` (`idProducto`, `id_Categoria_fk`, `nombre_producto`, `descripcion`, `stock`, `stock_minimo`, `precio_compra`, `precio_venta`) VALUES (6, 3, 'Amortiguador delantero', 'Amortiguador hidráulico para suspensión', 10, 4, '150000.00', '220000.00');
INSERT INTO `producto` (`idProducto`, `id_Categoria_fk`, `nombre_producto`, `descripcion`, `stock`, `stock_minimo`, `precio_compra`, `precio_venta`) VALUES (7, 3, 'Correa de transmision', 'Correa para motor 4 cilindros', 15, 6, '95000.00', '140000.00');
INSERT INTO `producto` (`idProducto`, `id_Categoria_fk`, `nombre_producto`, `descripcion`, `stock`, `stock_minimo`, `precio_compra`, `precio_venta`) VALUES (8, 3, 'Lámpara H4', 'Bombillo halógeno 12V para farola', 30, 10, '18000.00', '30000.00');

DROP TABLE IF EXISTS `producto_proveedor`;
CREATE TABLE `producto_proveedor` (
  `idProductoProveedor` int(11) NOT NULL AUTO_INCREMENT,
  `id_Producto_fk` int(11) NOT NULL,
  `id_Proveedor_fk` int(11) NOT NULL,
  PRIMARY KEY (`idProductoProveedor`),
  KEY `fk_pp_producto` (`id_Producto_fk`),
  KEY `fk_pp_proveedor` (`id_Proveedor_fk`),
  CONSTRAINT `fk_pp_producto` FOREIGN KEY (`id_Producto_fk`) REFERENCES `producto` (`idProducto`),
  CONSTRAINT `fk_pp_proveedor` FOREIGN KEY (`id_Proveedor_fk`) REFERENCES `proveedores` (`idProveedor`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `producto_proveedor` (`idProductoProveedor`, `id_Producto_fk`, `id_Proveedor_fk`) VALUES (1, 1, 2);
INSERT INTO `producto_proveedor` (`idProductoProveedor`, `id_Producto_fk`, `id_Proveedor_fk`) VALUES (2, 2, 1);
INSERT INTO `producto_proveedor` (`idProductoProveedor`, `id_Producto_fk`, `id_Proveedor_fk`) VALUES (3, 3, 3);
INSERT INTO `producto_proveedor` (`idProductoProveedor`, `id_Producto_fk`, `id_Proveedor_fk`) VALUES (4, 4, 5);
INSERT INTO `producto_proveedor` (`idProductoProveedor`, `id_Producto_fk`, `id_Proveedor_fk`) VALUES (5, 5, 4);
INSERT INTO `producto_proveedor` (`idProductoProveedor`, `id_Producto_fk`, `id_Proveedor_fk`) VALUES (6, 6, 3);
INSERT INTO `producto_proveedor` (`idProductoProveedor`, `id_Producto_fk`, `id_Proveedor_fk`) VALUES (7, 7, 1);
INSERT INTO `producto_proveedor` (`idProductoProveedor`, `id_Producto_fk`, `id_Proveedor_fk`) VALUES (8, 8, 2);

DROP TABLE IF EXISTS `proveedores`;
CREATE TABLE `proveedores` (
  `idProveedor` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `nit` varchar(20) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `direccion` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`idProveedor`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `proveedores` (`idProveedor`, `nombre`, `nit`, `telefono`, `direccion`) VALUES (1, 'Manuel Puertas (LumenX)', '900123456-7', '3104567890', 'Calle 45 #12-34, Bogotá');
INSERT INTO `proveedores` (`idProveedor`, `nombre`, `nit`, `telefono`, `direccion`) VALUES (2, 'Camilo Cruz (Power Light LED)', '901234567-8', '3115678901', 'Cra 15 #98-20, Medellín');
INSERT INTO `proveedores` (`idProveedor`, `nombre`, `nit`, `telefono`, `direccion`) VALUES (3, 'Mariana Zarate (Importadora Vanegas)', '902345678-9', '3126789012', 'Av 30 #45-10, Cali');
INSERT INTO `proveedores` (`idProveedor`, `nombre`, `nit`, `telefono`, `direccion`) VALUES (4, 'Nicolas Beltran (Sylvania Colombia)', '903456789-0', '3137890123', 'Calle 10 #22-18, Barranquilla');
INSERT INTO `proveedores` (`idProveedor`, `nombre`, `nit`, `telefono`, `direccion`) VALUES (5, 'Angie Torralba (Kingshowstar)', '904567890-1', '3148901234', 'Cra 8 #50-25, Bucaramanga');

DROP TABLE IF EXISTS `roles`;
CREATE TABLE `roles` (
  `idRol` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `descripcion` varchar(500) NOT NULL,
  `permisos` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`idRol`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `roles` (`idRol`, `nombre`, `descripcion`, `permisos`) VALUES (1, 'Super_administrador', 'Es el dueño del sistema y tiene control absoluto sobre todas las configuraciones y operaciones.', 'Acceso total e ilimitado al sistema; puede crear, modificar y eliminar usuarios, roles, productos y servicios, configurar el sistema, ver y generar todos los reportes, supervisar órdenes de servicio y realizar cualquier cambio sin restricciones.');
INSERT INTO `roles` (`idRol`, `nombre`, `descripcion`, `permisos`) VALUES (2, 'Administrador', 'Tiene control total del sistema. Gestionar usuarios, gestionar roles, administrar productos, ver reportes, modificar y eliminar registros.', 'Acceso casi total; puede crear, editar y eliminar usuarios, productos y órdenes de servicio y generar reportes.');
INSERT INTO `roles` (`idRol`, `nombre`, `descripcion`, `permisos`) VALUES (3, 'Cliente', 'Solo puede realizar compra y mantenimiento.', 'No tiene acceso alguno al programa.');
INSERT INTO `roles` (`idRol`, `nombre`, `descripcion`, `permisos`) VALUES (4, 'Mecanico', 'Encargado de realizar mantenimientos y reparaciones. Ver órdenes de servicio, actualizar estado de mantenimiento, registrar reparaciones.', 'Puede ver y gestionar órdenes de servicio asignadas, actualizar el estado del mantenimiento, registrar reparaciones realizadas, agregar observaciones técnicas, registrar repuestos utilizados y finalizar servicios.');

DROP TABLE IF EXISTS `tipo_movimiento`;
CREATE TABLE `tipo_movimiento` (
  `idTipoMovimiento` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`idTipoMovimiento`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `tipo_movimiento` (`idTipoMovimiento`, `nombre`, `descripcion`) VALUES (1, 'Entrada', 'Ingreso de productos al inventario');
INSERT INTO `tipo_movimiento` (`idTipoMovimiento`, `nombre`, `descripcion`) VALUES (2, 'Salida', 'Salida de productos por venta');
INSERT INTO `tipo_movimiento` (`idTipoMovimiento`, `nombre`, `descripcion`) VALUES (3, 'Devolucion', 'Producto devuelto por cliente');
INSERT INTO `tipo_movimiento` (`idTipoMovimiento`, `nombre`, `descripcion`) VALUES (4, 'Anulada', 'Corrección de inventario');

DROP TABLE IF EXISTS `tipo_servicio`;
CREATE TABLE `tipo_servicio` (
  `idTipoServicio` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  PRIMARY KEY (`idTipoServicio`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `tipo_servicio` (`idTipoServicio`, `nombre`) VALUES (1, 'Reparacion');
INSERT INTO `tipo_servicio` (`idTipoServicio`, `nombre`) VALUES (2, 'Venta');

DROP TABLE IF EXISTS `usuarios`;
CREATE TABLE `usuarios` (
  `idUsuario` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  `apellido` varchar(100) DEFAULT NULL,
  `contraseña` varchar(50) DEFAULT NULL,
  `correo` varchar(150) DEFAULT NULL,
  `id_Rol_fk` int(11) DEFAULT NULL,
  PRIMARY KEY (`idUsuario`),
  KEY `fk_usuario_rol` (`id_Rol_fk`),
  CONSTRAINT `fk_usuario_rol` FOREIGN KEY (`id_Rol_fk`) REFERENCES `roles` (`idRol`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `usuarios` (`idUsuario`, `nombre`, `apellido`, `contraseña`, `correo`, `id_Rol_fk`) VALUES (1, 'Luis Felipe', 'Puertas Castellar', 'JP2026*', 'luispuertas@gmail.com', 1);
INSERT INTO `usuarios` (`idUsuario`, `nombre`, `apellido`, `contraseña`, `correo`, `id_Rol_fk`) VALUES (2, 'Marcos Manuel', 'Puertas Julio', 'soytupapi1020', 'marcospuertas@gmail.com', 4);
INSERT INTO `usuarios` (`idUsuario`, `nombre`, `apellido`, `contraseña`, `correo`, `id_Rol_fk`) VALUES (3, 'Juan', 'Perez', 'ML$1234', 'juan.perez@gmail.com', 4);
INSERT INTO `usuarios` (`idUsuario`, `nombre`, `apellido`, `contraseña`, `correo`, `id_Rol_fk`) VALUES (4, 'Maria', 'Lopez', 'PJ14#', 'maria.lopez@hotmail.com', 2);
INSERT INTO `usuarios` (`idUsuario`, `nombre`, `apellido`, `contraseña`, `correo`, `id_Rol_fk`) VALUES (5, 'Miguel', 'Ramos', 'MTR#026', 'miguel.ramos@gmail.com', 4);
INSERT INTO `usuarios` (`idUsuario`, `nombre`, `apellido`, `contraseña`, `correo`, `id_Rol_fk`) VALUES (6, 'Pirlo', 'Antonio', NULL, NULL, 3);
INSERT INTO `usuarios` (`idUsuario`, `nombre`, `apellido`, `contraseña`, `correo`, `id_Rol_fk`) VALUES (7, 'Ryan', 'Castro', NULL, NULL, 3);
INSERT INTO `usuarios` (`idUsuario`, `nombre`, `apellido`, `contraseña`, `correo`, `id_Rol_fk`) VALUES (8, 'Gustavo', 'Petro', NULL, NULL, 3);
INSERT INTO `usuarios` (`idUsuario`, `nombre`, `apellido`, `contraseña`, `correo`, `id_Rol_fk`) VALUES (9, 'Neymar', 'Junior', NULL, NULL, 3);
INSERT INTO `usuarios` (`idUsuario`, `nombre`, `apellido`, `contraseña`, `correo`, `id_Rol_fk`) VALUES (10, 'Lamine', 'Yamal', NULL, NULL, 3);
INSERT INTO `usuarios` (`idUsuario`, `nombre`, `apellido`, `contraseña`, `correo`, `id_Rol_fk`) VALUES (12, 'ivan', 'cepeda', NULL, NULL, 3);

DROP TABLE IF EXISTS `vehiculos`;
CREATE TABLE `vehiculos` (
  `IDvehiculos` int(11) NOT NULL AUTO_INCREMENT,
  `id_Usuario_fk` int(11) NOT NULL,
  `id_Marca_fk` int(11) NOT NULL,
  `placa` varchar(15) NOT NULL,
  `modelo` varchar(50) DEFAULT NULL,
  `año` int(11) DEFAULT NULL,
  `color` varchar(15) NOT NULL,
  `tipo` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`IDvehiculos`),
  KEY `fk_vehiculo_usuario` (`id_Usuario_fk`),
  KEY `fk_vehiculo_marca` (`id_Marca_fk`),
  CONSTRAINT `fk_vehiculo_marca` FOREIGN KEY (`id_Marca_fk`) REFERENCES `marca_vehiculo` (`idMarca`),
  CONSTRAINT `fk_vehiculo_usuario` FOREIGN KEY (`id_Usuario_fk`) REFERENCES `usuarios` (`idUsuario`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `vehiculos` (`IDvehiculos`, `id_Usuario_fk`, `id_Marca_fk`, `placa`, `modelo`, `año`, `color`, `tipo`) VALUES (1, 6, 1, 'ABC123', 'Spark', 2020, 'Blanco', 'Automóvil');
INSERT INTO `vehiculos` (`IDvehiculos`, `id_Usuario_fk`, `id_Marca_fk`, `placa`, `modelo`, `año`, `color`, `tipo`) VALUES (2, 7, 2, 'DEF456', 'CX-5', 2022, 'Gris', 'Camioneta');
INSERT INTO `vehiculos` (`IDvehiculos`, `id_Usuario_fk`, `id_Marca_fk`, `placa`, `modelo`, `año`, `color`, `tipo`) VALUES (3, 8, 3, 'GHI789', 'Duster', 2021, 'Negro', 'Camioneta');
INSERT INTO `vehiculos` (`IDvehiculos`, `id_Usuario_fk`, `id_Marca_fk`, `placa`, `modelo`, `año`, `color`, `tipo`) VALUES (4, 9, 4, 'JKL321', 'Corolla', 2019, 'Rojo', 'Automóvil');
INSERT INTO `vehiculos` (`IDvehiculos`, `id_Usuario_fk`, `id_Marca_fk`, `placa`, `modelo`, `año`, `color`, `tipo`) VALUES (5, 10, 5, 'MNO654', 'Frontier', 2023, 'Azul', 'Pickup');
INSERT INTO `vehiculos` (`IDvehiculos`, `id_Usuario_fk`, `id_Marca_fk`, `placa`, `modelo`, `año`, `color`, `tipo`) VALUES (6, 12, 1, 'CDE321', 'Spark', NULL, '', 'Automóvil');

SET FOREIGN_KEY_CHECKS=1;
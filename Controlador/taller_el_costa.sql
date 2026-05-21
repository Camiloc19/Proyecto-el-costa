-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 20-05-2026 a las 17:04:50
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `taller_el_costa`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `atencion_vehiculo`
--

CREATE TABLE `atencion_vehiculo` (
  `idAtencion` int(11) NOT NULL,
  `id_Vehiculo_fk` int(11) NOT NULL,
  `id_Usuario_fk` int(11) NOT NULL,
  `id_Rol_fk` int(11) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_final` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `atencion_vehiculo`
--

INSERT INTO `atencion_vehiculo` (`idAtencion`, `id_Vehiculo_fk`, `id_Usuario_fk`, `id_Rol_fk`, `fecha_inicio`, `fecha_final`) VALUES
(1, 1, 2, 4, '2026-03-23', '2026-03-25'),
(2, 2, 3, 4, '2026-02-18', '2026-03-24'),
(3, 3, 2, 4, '2026-01-04', '2026-01-06'),
(4, 4, 3, 4, '2026-01-15', '2026-01-17'),
(5, 5, 4, 4, '2026-01-30', '2026-02-05');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categoria_producto`
--

CREATE TABLE `categoria_producto` (
  `idCategoria` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `categoria_producto`
--

INSERT INTO `categoria_producto` (`idCategoria`, `nombre`, `descripcion`) VALUES
(1, 'Filtros', 'Retiene impurezas en los sistemas del vehiculo'),
(2, 'Lujos', 'Mejoran la funcionalidad, comodidad y estetica del vehiculo'),
(3, 'Repuestos', 'Piezas para remplazar componentes dañados o gastados'),
(4, 'Llantas', 'Componentes de caucho para el trayecto y frenado'),
(5, 'Aceites', 'Lubricantes para proteger los componentes mecanicos');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_movimiento`
--

CREATE TABLE `detalle_movimiento` (
  `idMovimiento` int(11) NOT NULL,
  `id_TipoMovimiento_fk` int(11) NOT NULL,
  `id_Factura_fk` int(11) NOT NULL,
  `id_ProductoProveedor_fk` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `detalle_movimiento`
--

INSERT INTO `detalle_movimiento` (`idMovimiento`, `id_TipoMovimiento_fk`, `id_Factura_fk`, `id_ProductoProveedor_fk`, `cantidad`) VALUES
(1, 2, 1, 1, 1),
(2, 2, 2, 4, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_orden`
--

CREATE TABLE `detalle_orden` (
  `idDetalleServicio` int(11) NOT NULL,
  `id_Orden_fk` int(11) NOT NULL,
  `id_TipoServicio_fk` int(11) NOT NULL,
  `id_Producto_fk` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `detalle_orden`
--

INSERT INTO `detalle_orden` (`idDetalleServicio`, `id_Orden_fk`, `id_TipoServicio_fk`, `id_Producto_fk`, `cantidad`, `precio_unitario`) VALUES
(1, 1, 1, 1, 1, 45000.00),
(2, 2, 2, 2, 2, 30000.00),
(3, 3, 2, 3, 3, 140000.00),
(4, 4, 1, 4, 1, 30000.00),
(5, 5, 1, 5, 2, 220000.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estado_orden`
--

CREATE TABLE `estado_orden` (
  `idEstado` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `estado_orden`
--

INSERT INTO `estado_orden` (`idEstado`, `nombre`) VALUES
(1, 'En proceso'),
(2, 'Finalizado');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `factura`
--

CREATE TABLE `factura` (
  `idFactura` int(11) NOT NULL,
  `id_Orden_fk` int(11) NOT NULL,
  `id_MetodoPago_fk` int(11) NOT NULL,
  `numero_factura` varchar(20) NOT NULL,
  `fecha` date NOT NULL,
  `total` decimal(12,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `factura`
--

INSERT INTO `factura` (`idFactura`, `id_Orden_fk`, `id_MetodoPago_fk`, `numero_factura`, `fecha`, `total`) VALUES
(1, 1, 1, '1001', '2026-03-04', 250000.00),
(2, 2, 2, '1002', '2026-03-04', 180000.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `marca_vehiculo`
--

CREATE TABLE `marca_vehiculo` (
  `idMarca` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `marca_vehiculo`
--

INSERT INTO `marca_vehiculo` (`idMarca`, `nombre`) VALUES
(1, 'Chevrolet'),
(2, 'Mazda'),
(3, 'Renault'),
(4, 'Toyota'),
(5, 'Nissan');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `metodo_pago`
--

CREATE TABLE `metodo_pago` (
  `idMetodoPago` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `metodo_pago`
--

INSERT INTO `metodo_pago` (`idMetodoPago`, `nombre`) VALUES
(1, 'Efectivo'),
(2, 'Nequi');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `orden_servicio`
--

CREATE TABLE `orden_servicio` (
  `Id_orden` int(11) NOT NULL,
  `id_Vehiculo_fk` int(11) NOT NULL,
  `id_Usuario_fk` int(11) NOT NULL,
  `id_Estado_fk` int(11) NOT NULL,
  `numero_orden` varchar(50) NOT NULL,
  `hora_apertura` varchar(20) DEFAULT NULL,
  `fecha_apertura` date NOT NULL,
  `fecha_cierre` date DEFAULT NULL,
  `total` decimal(12,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `orden_servicio`
--

INSERT INTO `orden_servicio` (`Id_orden`, `id_Vehiculo_fk`, `id_Usuario_fk`, `id_Estado_fk`, `numero_orden`, `hora_apertura`, `fecha_apertura`, `fecha_cierre`, `total`) VALUES
(1, 1, 6, 1, '5001', '08:00 AM', '2026-03-02', '2026-03-04', 250000.00),
(2, 2, 7, 1, '5002', '09:30 AM', '2026-03-13', '2026-03-15', 180000.00),
(3, 3, 8, 1, '5003', '10:15 AM', '2026-03-04', '2026-03-06', NULL),
(4, 4, 9, 1, '5004', '12:00 PM', '2026-03-15', '2026-03-17', NULL),
(5, 5, 10, 2, '5005', '02:22 PM', '2026-03-17', '2026-03-19', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto`
--

CREATE TABLE `producto` (
  `idProducto` int(11) NOT NULL,
  `id_Categoria_fk` int(11) NOT NULL,
  `nombre_producto` varchar(150) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `stock` int(11) NOT NULL DEFAULT 0,
  `stock_minimo` int(11) NOT NULL DEFAULT 0,
  `precio_compra` decimal(10,2) NOT NULL,
  `precio_venta` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `producto`
--

INSERT INTO `producto` (`idProducto`, `id_Categoria_fk`, `nombre_producto`, `descripcion`, `stock`, `stock_minimo`, `precio_compra`, `precio_venta`) VALUES
(1, 5, 'Filtro de aceite', 'Filtro para motor 1.6L - 2.0L', 25, 10, 45000.00, 70000.00),
(2, 2, 'Pastillas de freno', 'Juego delantero para automóvil sedan', 18, 18, 120000.00, 180000.00),
(3, 3, 'Batería 12V 60Ah', 'Batería automotriz libre mantenimiento', 12, 5, 280000.00, 360000.00),
(4, 5, 'Aceite 10W-40', 'Aceite sintético para motor - 1 litro', 40, 15, 30000.00, 45000.00),
(5, 3, 'Bujía estándar', 'Bujía para motor gasolina', 50, 20, 12000.00, 20000.00),
(6, 3, 'Amortiguador delantero', 'Amortiguador hidráulico para suspensión', 10, 4, 150000.00, 220000.00),
(7, 3, 'Correa de transmision', 'Correa para motor 4 cilindros', 15, 6, 95000.00, 140000.00),
(8, 3, 'Lámpara H4', 'Bombillo halógeno 12V para farola', 30, 10, 18000.00, 30000.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto_proveedor`
--

CREATE TABLE `producto_proveedor` (
  `idProductoProveedor` int(11) NOT NULL,
  `id_Producto_fk` int(11) NOT NULL,
  `id_Proveedor_fk` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `producto_proveedor`
--

INSERT INTO `producto_proveedor` (`idProductoProveedor`, `id_Producto_fk`, `id_Proveedor_fk`) VALUES
(1, 1, 2),
(2, 2, 1),
(3, 3, 3),
(4, 4, 5),
(5, 5, 4),
(6, 6, 3),
(7, 7, 1),
(8, 8, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedores`
--

CREATE TABLE `proveedores` (
  `idProveedor` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `nit` varchar(20) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `direccion` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `proveedores`
--

INSERT INTO `proveedores` (`idProveedor`, `nombre`, `nit`, `telefono`, `direccion`) VALUES
(1, 'Manuel Puertas (LumenX)', '900123456-7', '3104567890', 'Calle 45 #12-34, Bogotá'),
(2, 'Camilo Cruz (Power Light LED)', '901234567-8', '3115678901', 'Cra 15 #98-20, Medellín'),
(3, 'Mariana Zarate (Importadora Vanegas)', '902345678-9', '3126789012', 'Av 30 #45-10, Cali'),
(4, 'Nicolas Beltran (Sylvania Colombia)', '903456789-0', '3137890123', 'Calle 10 #22-18, Barranquilla'),
(5, 'Angie Torralba (Kingshowstar)', '904567890-1', '3148901234', 'Cra 8 #50-25, Bucaramanga');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `idRol` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `descripcion` varchar(500) NOT NULL,
  `permisos` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`idRol`, `nombre`, `descripcion`, `permisos`) VALUES
(1, 'Super_administrador', 'Es el dueño del sistema y tiene control absoluto sobre todas las configuraciones y operaciones.', 'Acceso total e ilimitado al sistema; puede crear, modificar y eliminar usuarios, roles, productos y servicios, configurar el sistema, ver y generar todos los reportes, supervisar órdenes de servicio y realizar cualquier cambio sin restricciones.'),
(2, 'Administrador', 'Tiene control total del sistema. Gestionar usuarios, gestionar roles, administrar productos, ver reportes, modificar y eliminar registros.', 'Acceso casi total; puede crear, editar y eliminar usuarios, productos y órdenes de servicio y generar reportes.'),
(3, 'Cliente', 'Solo puede realizar compra y mantenimiento.', 'No tiene acceso alguno al programa.'),
(4, 'Mecanico', 'Encargado de realizar mantenimientos y reparaciones. Ver órdenes de servicio, actualizar estado de mantenimiento, registrar reparaciones.', 'Puede ver y gestionar órdenes de servicio asignadas, actualizar el estado del mantenimiento, registrar reparaciones realizadas, agregar observaciones técnicas, registrar repuestos utilizados y finalizar servicios.');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_movimiento`
--

CREATE TABLE `tipo_movimiento` (
  `idTipoMovimiento` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tipo_movimiento`
--

INSERT INTO `tipo_movimiento` (`idTipoMovimiento`, `nombre`, `descripcion`) VALUES
(1, 'Entrada', 'Ingreso de productos al inventario'),
(2, 'Salida', 'Salida de productos por venta'),
(3, 'Devolucion', 'Producto devuelto por cliente'),
(4, 'Anulada', 'Corrección de inventario');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_servicio`
--

CREATE TABLE `tipo_servicio` (
  `idTipoServicio` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tipo_servicio`
--

INSERT INTO `tipo_servicio` (`idTipoServicio`, `nombre`) VALUES
(1, 'Reparacion'),
(2, 'Venta');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `idUsuario` int(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `apellido` varchar(100) DEFAULT NULL,
  `contraseña` varchar(50) DEFAULT NULL,
  `correo` varchar(150) DEFAULT NULL,
  `id_Rol_fk` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`idUsuario`, `nombre`, `apellido`, `contraseña`, `correo`, `id_Rol_fk`) VALUES
(1, 'Luis Felipe', 'Puertas Castellar', 'JP2026*', 'luispuertas@gmail.com', 1),
(2, 'Marcos Manuel', 'Puertas Julio', 'soytupapi1020', 'marcospuertas@gmail.com', 4),
(3, 'Juan', 'Perez', 'ML$1234', 'juan.perez@gmail.com', 4),
(4, 'Maria', 'Lopez', 'PJ14#', 'maria.lopez@hotmail.com', 2),
(5, 'Miguel', 'Ramos', 'MTR#026', 'miguel.ramos@gmail.com', 4),
(6, 'Pirlo', 'Antonio', NULL, NULL, 3),
(7, 'Ryan', 'Castro', NULL, NULL, 3),
(8, 'Gustavo', 'Petro', NULL, NULL, 3),
(9, 'Neymar', 'Junior', NULL, NULL, 3),
(10, 'Lamine', 'Yamal', NULL, NULL, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `vehiculos`
--

CREATE TABLE `vehiculos` (
  `IDvehiculos` int(11) NOT NULL,
  `id_Usuario_fk` int(11) NOT NULL,
  `id_Marca_fk` int(11) NOT NULL,
  `placa` varchar(15) NOT NULL,
  `modelo` varchar(50) DEFAULT NULL,
  `año` int(11) DEFAULT NULL,
  `color` varchar(15) NOT NULL,
  `tipo` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `vehiculos`
--

INSERT INTO `vehiculos` (`IDvehiculos`, `id_Usuario_fk`, `id_Marca_fk`, `placa`, `modelo`, `año`, `color`, `tipo`) VALUES
(1, 6, 1, 'ABC123', 'Spark', 2020, 'Blanco', 'Automóvil'),
(2, 7, 2, 'DEF456', 'CX-5', 2022, 'Gris', 'Camioneta'),
(3, 8, 3, 'GHI789', 'Duster', 2021, 'Negro', 'Camioneta'),
(4, 9, 4, 'JKL321', 'Corolla', 2019, 'Rojo', 'Automóvil'),
(5, 10, 5, 'MNO654', 'Frontier', 2023, 'Azul', 'Pickup');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `atencion_vehiculo`
--
ALTER TABLE `atencion_vehiculo`
  ADD PRIMARY KEY (`idAtencion`),
  ADD KEY `fk_atencion_vehiculo` (`id_Vehiculo_fk`),
  ADD KEY `fk_atencion_usuario` (`id_Usuario_fk`),
  ADD KEY `fk_atencion_rol` (`id_Rol_fk`);

--
-- Indices de la tabla `categoria_producto`
--
ALTER TABLE `categoria_producto`
  ADD PRIMARY KEY (`idCategoria`);

--
-- Indices de la tabla `detalle_movimiento`
--
ALTER TABLE `detalle_movimiento`
  ADD PRIMARY KEY (`idMovimiento`),
  ADD KEY `fk_detmov_tipo` (`id_TipoMovimiento_fk`),
  ADD KEY `fk_detmov_factura` (`id_Factura_fk`),
  ADD KEY `fk_detmov_prodprov` (`id_ProductoProveedor_fk`);

--
-- Indices de la tabla `detalle_orden`
--
ALTER TABLE `detalle_orden`
  ADD PRIMARY KEY (`idDetalleServicio`),
  ADD KEY `fk_detalle_orden` (`id_Orden_fk`),
  ADD KEY `fk_detalle_tiposervicio` (`id_TipoServicio_fk`),
  ADD KEY `fk_detalle_producto` (`id_Producto_fk`);

--
-- Indices de la tabla `estado_orden`
--
ALTER TABLE `estado_orden`
  ADD PRIMARY KEY (`idEstado`);

--
-- Indices de la tabla `factura`
--
ALTER TABLE `factura`
  ADD PRIMARY KEY (`idFactura`),
  ADD KEY `fk_factura_orden` (`id_Orden_fk`),
  ADD KEY `fk_factura_metodo` (`id_MetodoPago_fk`);

--
-- Indices de la tabla `marca_vehiculo`
--
ALTER TABLE `marca_vehiculo`
  ADD PRIMARY KEY (`idMarca`);

--
-- Indices de la tabla `metodo_pago`
--
ALTER TABLE `metodo_pago`
  ADD PRIMARY KEY (`idMetodoPago`);

--
-- Indices de la tabla `orden_servicio`
--
ALTER TABLE `orden_servicio`
  ADD PRIMARY KEY (`Id_orden`),
  ADD KEY `fk_orden_vehiculo` (`id_Vehiculo_fk`),
  ADD KEY `fk_orden_usuario` (`id_Usuario_fk`),
  ADD KEY `fk_orden_estado` (`id_Estado_fk`);

--
-- Indices de la tabla `producto`
--
ALTER TABLE `producto`
  ADD PRIMARY KEY (`idProducto`),
  ADD KEY `fk_producto_categoria` (`id_Categoria_fk`);

--
-- Indices de la tabla `producto_proveedor`
--
ALTER TABLE `producto_proveedor`
  ADD PRIMARY KEY (`idProductoProveedor`),
  ADD KEY `fk_pp_producto` (`id_Producto_fk`),
  ADD KEY `fk_pp_proveedor` (`id_Proveedor_fk`);

--
-- Indices de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  ADD PRIMARY KEY (`idProveedor`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`idRol`);

--
-- Indices de la tabla `tipo_movimiento`
--
ALTER TABLE `tipo_movimiento`
  ADD PRIMARY KEY (`idTipoMovimiento`);

--
-- Indices de la tabla `tipo_servicio`
--
ALTER TABLE `tipo_servicio`
  ADD PRIMARY KEY (`idTipoServicio`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`idUsuario`),
  ADD KEY `fk_usuario_rol` (`id_Rol_fk`);

--
-- Indices de la tabla `vehiculos`
--
ALTER TABLE `vehiculos`
  ADD PRIMARY KEY (`IDvehiculos`),
  ADD KEY `fk_vehiculo_usuario` (`id_Usuario_fk`),
  ADD KEY `fk_vehiculo_marca` (`id_Marca_fk`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `atencion_vehiculo`
--
ALTER TABLE `atencion_vehiculo`
  MODIFY `idAtencion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `categoria_producto`
--
ALTER TABLE `categoria_producto`
  MODIFY `idCategoria` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `detalle_movimiento`
--
ALTER TABLE `detalle_movimiento`
  MODIFY `idMovimiento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `detalle_orden`
--
ALTER TABLE `detalle_orden`
  MODIFY `idDetalleServicio` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `estado_orden`
--
ALTER TABLE `estado_orden`
  MODIFY `idEstado` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `factura`
--
ALTER TABLE `factura`
  MODIFY `idFactura` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `marca_vehiculo`
--
ALTER TABLE `marca_vehiculo`
  MODIFY `idMarca` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `metodo_pago`
--
ALTER TABLE `metodo_pago`
  MODIFY `idMetodoPago` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `orden_servicio`
--
ALTER TABLE `orden_servicio`
  MODIFY `Id_orden` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `producto`
--
ALTER TABLE `producto`
  MODIFY `idProducto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `producto_proveedor`
--
ALTER TABLE `producto_proveedor`
  MODIFY `idProductoProveedor` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  MODIFY `idProveedor` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `idRol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `tipo_movimiento`
--
ALTER TABLE `tipo_movimiento`
  MODIFY `idTipoMovimiento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `tipo_servicio`
--
ALTER TABLE `tipo_servicio`
  MODIFY `idTipoServicio` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `idUsuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `vehiculos`
--
ALTER TABLE `vehiculos`
  MODIFY `IDvehiculos` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `atencion_vehiculo`
--
ALTER TABLE `atencion_vehiculo`
  ADD CONSTRAINT `fk_atencion_rol` FOREIGN KEY (`id_Rol_fk`) REFERENCES `roles` (`idRol`),
  ADD CONSTRAINT `fk_atencion_usuario` FOREIGN KEY (`id_Usuario_fk`) REFERENCES `usuarios` (`idUsuario`),
  ADD CONSTRAINT `fk_atencion_vehiculo` FOREIGN KEY (`id_Vehiculo_fk`) REFERENCES `vehiculos` (`IDvehiculos`);

--
-- Filtros para la tabla `detalle_movimiento`
--
ALTER TABLE `detalle_movimiento`
  ADD CONSTRAINT `fk_detmov_factura` FOREIGN KEY (`id_Factura_fk`) REFERENCES `factura` (`idFactura`),
  ADD CONSTRAINT `fk_detmov_prodprov` FOREIGN KEY (`id_ProductoProveedor_fk`) REFERENCES `producto_proveedor` (`idProductoProveedor`),
  ADD CONSTRAINT `fk_detmov_tipo` FOREIGN KEY (`id_TipoMovimiento_fk`) REFERENCES `tipo_movimiento` (`idTipoMovimiento`);

--
-- Filtros para la tabla `detalle_orden`
--
ALTER TABLE `detalle_orden`
  ADD CONSTRAINT `fk_detalle_orden` FOREIGN KEY (`id_Orden_fk`) REFERENCES `orden_servicio` (`Id_orden`),
  ADD CONSTRAINT `fk_detalle_producto` FOREIGN KEY (`id_Producto_fk`) REFERENCES `producto` (`idProducto`),
  ADD CONSTRAINT `fk_detalle_tiposervicio` FOREIGN KEY (`id_TipoServicio_fk`) REFERENCES `tipo_servicio` (`idTipoServicio`);

--
-- Filtros para la tabla `factura`
--
ALTER TABLE `factura`
  ADD CONSTRAINT `fk_factura_metodo` FOREIGN KEY (`id_MetodoPago_fk`) REFERENCES `metodo_pago` (`idMetodoPago`),
  ADD CONSTRAINT `fk_factura_orden` FOREIGN KEY (`id_Orden_fk`) REFERENCES `orden_servicio` (`Id_orden`);

--
-- Filtros para la tabla `orden_servicio`
--
ALTER TABLE `orden_servicio`
  ADD CONSTRAINT `fk_orden_estado` FOREIGN KEY (`id_Estado_fk`) REFERENCES `estado_orden` (`idEstado`),
  ADD CONSTRAINT `fk_orden_usuario` FOREIGN KEY (`id_Usuario_fk`) REFERENCES `usuarios` (`idUsuario`),
  ADD CONSTRAINT `fk_orden_vehiculo` FOREIGN KEY (`id_Vehiculo_fk`) REFERENCES `vehiculos` (`IDvehiculos`);

--
-- Filtros para la tabla `producto`
--
ALTER TABLE `producto`
  ADD CONSTRAINT `fk_producto_categoria` FOREIGN KEY (`id_Categoria_fk`) REFERENCES `categoria_producto` (`idCategoria`);

--
-- Filtros para la tabla `producto_proveedor`
--
ALTER TABLE `producto_proveedor`
  ADD CONSTRAINT `fk_pp_producto` FOREIGN KEY (`id_Producto_fk`) REFERENCES `producto` (`idProducto`),
  ADD CONSTRAINT `fk_pp_proveedor` FOREIGN KEY (`id_Proveedor_fk`) REFERENCES `proveedores` (`idProveedor`);

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `fk_usuario_rol` FOREIGN KEY (`id_Rol_fk`) REFERENCES `roles` (`idRol`);

--
-- Filtros para la tabla `vehiculos`
--
ALTER TABLE `vehiculos`
  ADD CONSTRAINT `fk_vehiculo_marca` FOREIGN KEY (`id_Marca_fk`) REFERENCES `marca_vehiculo` (`idMarca`),
  ADD CONSTRAINT `fk_vehiculo_usuario` FOREIGN KEY (`id_Usuario_fk`) REFERENCES `usuarios` (`idUsuario`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

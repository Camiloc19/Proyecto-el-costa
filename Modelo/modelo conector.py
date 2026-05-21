import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="taller_el_costa"
    )


# ═════════════════════════════════════════
#  USUARIOS
# ═════════════════════════════════════════

def obtener_usuarios():
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("""
        SELECT u.*, r.nombre AS rol 
        FROM usuarios u 
        LEFT JOIN roles r ON u.id_Rol_fk = r.idRol
    """)
    resultado = cursor.fetchall()
    con.close()
    return resultado

def login_usuario(correo, contrasena):
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("""
        SELECT u.*, r.nombre AS rol 
        FROM usuarios u 
        LEFT JOIN roles r ON u.id_Rol_fk = r.idRol
        WHERE u.correo = %s AND u.contraseña = %s
    """, (correo, contrasena))
    resultado = cursor.fetchone()
    con.close()
    return resultado

def crear_usuario(nombre, apellido, contrasena, correo, id_rol):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO usuarios (nombre, apellido, contraseña, correo, id_Rol_fk) 
        VALUES (%s, %s, %s, %s, %s)
    """, (nombre, apellido, contrasena, correo, id_rol))
    con.commit()
    con.close()

def actualizar_usuario(id, nombre, apellido, contrasena, correo, id_rol):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("""
        UPDATE usuarios SET nombre=%s, apellido=%s, contraseña=%s, correo=%s, id_Rol_fk=%s 
        WHERE idUsuario=%s
    """, (nombre, apellido, contrasena, correo, id_rol, id))
    con.commit()
    con.close()

def eliminar_usuario(id):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("DELETE FROM usuarios WHERE idUsuario=%s", (id,))
    con.commit()
    con.close()

def obtener_roles():
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM roles")
    resultado = cursor.fetchall()
    con.close()
    return resultado


# ═════════════════════════════════════════
#  VEHÍCULOS
# ═════════════════════════════════════════

def obtener_vehiculos():
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("""
        SELECT v.*, 
               CONCAT(u.nombre, ' ', u.apellido) AS propietario,
               m.nombre AS marca
        FROM vehiculos v
        LEFT JOIN usuarios u      ON v.id_Usuario_fk = u.idUsuario
        LEFT JOIN marca_vehiculo m ON v.id_Marca_fk   = m.idMarca
    """)
    resultado = cursor.fetchall()
    con.close()
    return resultado

def obtener_vehiculo_por_id(id):
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("""
        SELECT v.*, 
               CONCAT(u.nombre, ' ', u.apellido) AS propietario,
               m.nombre AS marca
        FROM vehiculos v
        LEFT JOIN usuarios u      ON v.id_Usuario_fk = u.idUsuario
        LEFT JOIN marca_vehiculo m ON v.id_Marca_fk   = m.idMarca
        WHERE v.IDvehiculos = %s
    """, (id,))
    resultado = cursor.fetchone()
    con.close()
    return resultado

def crear_vehiculo(id_usuario, id_marca, placa, modelo, año, color, tipo):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO vehiculos (id_Usuario_fk, id_Marca_fk, placa, modelo, año, color, tipo) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (id_usuario, id_marca, placa, modelo, año, color, tipo))
    con.commit()
    con.close()

def actualizar_vehiculo(id, id_usuario, id_marca, placa, modelo, año, color, tipo):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("""
        UPDATE vehiculos SET id_Usuario_fk=%s, id_Marca_fk=%s, placa=%s, modelo=%s, año=%s, color=%s, tipo=%s 
        WHERE IDvehiculos=%s
    """, (id_usuario, id_marca, placa, modelo, año, color, tipo, id))
    con.commit()
    con.close()

def eliminar_vehiculo(id):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("DELETE FROM vehiculos WHERE IDvehiculos=%s", (id,))
    con.commit()
    con.close()

def obtener_marcas():
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM marca_vehiculo")
    resultado = cursor.fetchall()
    con.close()
    return resultado


# ═════════════════════════════════════════
#  ÓRDENES DE SERVICIO
# ═════════════════════════════════════════

def obtener_ordenes():
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("""
        SELECT os.*, 
               v.placa,
               CONCAT(u.nombre, ' ', u.apellido) AS cliente,
               e.nombre AS estado
        FROM orden_servicio os
        LEFT JOIN vehiculos v    ON os.id_Vehiculo_fk = v.IDvehiculos
        LEFT JOIN usuarios u     ON os.id_Usuario_fk  = u.idUsuario
        LEFT JOIN estado_orden e ON os.id_Estado_fk   = e.idEstado
        ORDER BY os.fecha_apertura DESC
    """)
    resultado = cursor.fetchall()
    con.close()
    return resultado

def obtener_orden_por_id(id):
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("""
        SELECT os.*, 
               v.placa,
               CONCAT(u.nombre, ' ', u.apellido) AS cliente,
               e.nombre AS estado
        FROM orden_servicio os
        LEFT JOIN vehiculos v    ON os.id_Vehiculo_fk = v.IDvehiculos
        LEFT JOIN usuarios u     ON os.id_Usuario_fk  = u.idUsuario
        LEFT JOIN estado_orden e ON os.id_Estado_fk   = e.idEstado
        WHERE os.Id_orden = %s
    """, (id,))
    resultado = cursor.fetchone()
    con.close()
    return resultado

def crear_orden(id_vehiculo, id_usuario, id_estado, numero_orden, hora_apertura, fecha_apertura):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO orden_servicio (id_Vehiculo_fk, id_Usuario_fk, id_Estado_fk, numero_orden, hora_apertura, fecha_apertura) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (id_vehiculo, id_usuario, id_estado, numero_orden, hora_apertura, fecha_apertura))
    con.commit()
    con.close()

def actualizar_estado_orden(id, id_estado, fecha_cierre, total):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("""
        UPDATE orden_servicio SET id_Estado_fk=%s, fecha_cierre=%s, total=%s 
        WHERE Id_orden=%s
    """, (id_estado, fecha_cierre, total, id))
    con.commit()
    con.close()

def eliminar_orden(id):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("DELETE FROM orden_servicio WHERE Id_orden=%s", (id,))
    con.commit()
    con.close()

def obtener_estados_orden():
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM estado_orden")
    resultado = cursor.fetchall()
    con.close()
    return resultado


# ═════════════════════════════════════════
#  DETALLE DE ORDEN
# ═════════════════════════════════════════

def obtener_detalle_orden(id_orden):
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("""
        SELECT d.*, 
               p.nombre_producto,
               ts.nombre AS tipo_servicio
        FROM detalle_orden d
        LEFT JOIN producto p       ON d.id_Producto_fk     = p.idProducto
        LEFT JOIN tipo_servicio ts ON d.id_TipoServicio_fk = ts.idTipoServicio
        WHERE d.id_Orden_fk = %s
    """, (id_orden,))
    resultado = cursor.fetchall()
    con.close()
    return resultado

def agregar_detalle_orden(id_orden, id_tipo_servicio, id_producto, cantidad, precio_unitario):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO detalle_orden (id_Orden_fk, id_TipoServicio_fk, id_Producto_fk, cantidad, precio_unitario) 
        VALUES (%s, %s, %s, %s, %s)
    """, (id_orden, id_tipo_servicio, id_producto, cantidad, precio_unitario))
    con.commit()
    con.close()

def obtener_tipos_servicio():
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tipo_servicio")
    resultado = cursor.fetchall()
    con.close()
    return resultado


# ═════════════════════════════════════════
#  PRODUCTOS / INVENTARIO
# ═════════════════════════════════════════

def obtener_productos():
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.*, c.nombre AS categoria
        FROM producto p
        LEFT JOIN categoria_producto c ON p.id_Categoria_fk = c.idCategoria
        ORDER BY p.nombre_producto
    """)
    resultado = cursor.fetchall()
    con.close()
    return resultado

def obtener_producto_por_id(id):
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.*, c.nombre AS categoria
        FROM producto p
        LEFT JOIN categoria_producto c ON p.id_Categoria_fk = c.idCategoria
        WHERE p.idProducto = %s
    """, (id,))
    resultado = cursor.fetchone()
    con.close()
    return resultado

def crear_producto(id_categoria, nombre, descripcion, stock, stock_minimo, precio_compra, precio_venta):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO producto (id_Categoria_fk, nombre_producto, descripcion, stock, stock_minimo, precio_compra, precio_venta) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (id_categoria, nombre, descripcion, stock, stock_minimo, precio_compra, precio_venta))
    con.commit()
    con.close()

def actualizar_producto(id, id_categoria, nombre, descripcion, stock, stock_minimo, precio_compra, precio_venta):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("""
        UPDATE producto SET id_Categoria_fk=%s, nombre_producto=%s, descripcion=%s, 
               stock=%s, stock_minimo=%s, precio_compra=%s, precio_venta=%s 
        WHERE idProducto=%s
    """, (id_categoria, nombre, descripcion, stock, stock_minimo, precio_compra, precio_venta, id))
    con.commit()
    con.close()

def eliminar_producto(id):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("DELETE FROM producto WHERE idProducto=%s", (id,))
    con.commit()
    con.close()

def obtener_productos_bajo_stock():
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM producto WHERE stock <= stock_minimo")
    resultado = cursor.fetchall()
    con.close()
    return resultado

def obtener_categorias():
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categoria_producto")
    resultado = cursor.fetchall()
    con.close()
    return resultado


# ═════════════════════════════════════════
#  FACTURAS
# ═════════════════════════════════════════

def obtener_facturas():
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("""
        SELECT f.*, 
               os.numero_orden,
               mp.nombre AS metodo_pago
        FROM factura f
        LEFT JOIN orden_servicio os ON f.id_Orden_fk      = os.Id_orden
        LEFT JOIN metodo_pago mp    ON f.id_MetodoPago_fk = mp.idMetodoPago
        ORDER BY f.fecha DESC
    """)
    resultado = cursor.fetchall()
    con.close()
    return resultado

def obtener_factura_por_id(id):
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("""
        SELECT f.*, 
               os.numero_orden,
               mp.nombre AS metodo_pago
        FROM factura f
        LEFT JOIN orden_servicio os ON f.id_Orden_fk      = os.Id_orden
        LEFT JOIN metodo_pago mp    ON f.id_MetodoPago_fk = mp.idMetodoPago
        WHERE f.idFactura = %s
    """, (id,))
    resultado = cursor.fetchone()
    con.close()
    return resultado

def crear_factura(id_orden, id_metodo_pago, numero_factura, fecha, total):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO factura (id_Orden_fk, id_MetodoPago_fk, numero_factura, fecha, total) 
        VALUES (%s, %s, %s, %s, %s)
    """, (id_orden, id_metodo_pago, numero_factura, fecha, total))
    con.commit()
    con.close()

def obtener_metodos_pago():
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM metodo_pago")
    resultado = cursor.fetchall()
    con.close()
    return resultado


# ═════════════════════════════════════════
#  PROVEEDORES
# ═════════════════════════════════════════

def obtener_proveedores():
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM proveedores")
    resultado = cursor.fetchall()
    con.close()
    return resultado

def crear_proveedor(nombre, nit, telefono, direccion):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO proveedores (nombre, nit, telefono, direccion) 
        VALUES (%s, %s, %s, %s)
    """, (nombre, nit, telefono, direccion))
    con.commit()
    con.close()

def actualizar_proveedor(id, nombre, nit, telefono, direccion):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("""
        UPDATE proveedores SET nombre=%s, nit=%s, telefono=%s, direccion=%s 
        WHERE idProveedor=%s
    """, (nombre, nit, telefono, direccion, id))
    con.commit()
    con.close()

def eliminar_proveedor(id):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("DELETE FROM proveedores WHERE idProveedor=%s", (id,))
    con.commit()
    con.close()


# ═════════════════════════════════════════
#  MOVIMIENTOS DE INVENTARIO
# ═════════════════════════════════════════

def obtener_movimientos():
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("""
        SELECT dm.*, 
               tm.nombre AS tipo_movimiento,
               f.numero_factura,
               p.nombre_producto
        FROM detalle_movimiento dm
        LEFT JOIN tipo_movimiento tm    ON dm.id_TipoMovimiento_fk    = tm.idTipoMovimiento
        LEFT JOIN factura f             ON dm.id_Factura_fk           = f.idFactura
        LEFT JOIN producto_proveedor pp ON dm.id_ProductoProveedor_fk = pp.idProductoProveedor
        LEFT JOIN producto p            ON pp.id_Producto_fk          = p.idProducto
    """)
    resultado = cursor.fetchall()
    con.close()
    return resultado

def registrar_movimiento(id_tipo_movimiento, id_factura, id_producto_proveedor, cantidad):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO detalle_movimiento (id_TipoMovimiento_fk, id_Factura_fk, id_ProductoProveedor_fk, cantidad) 
        VALUES (%s, %s, %s, %s)
    """, (id_tipo_movimiento, id_factura, id_producto_proveedor, cantidad))
    con.commit()
    con.close()

def obtener_tipos_movimiento():
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tipo_movimiento")
    resultado = cursor.fetchall()
    con.close()
    return resultado


# ═════════════════════════════════════════
#  ATENCIÓN DE VEHÍCULOS
# ═════════════════════════════════════════

def obtener_atenciones():
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("""
        SELECT av.*, 
               v.placa,
               CONCAT(u.nombre, ' ', u.apellido) AS mecanico,
               r.nombre AS rol
        FROM atencion_vehiculo av
        LEFT JOIN vehiculos v ON av.id_Vehiculo_fk = v.IDvehiculos
        LEFT JOIN usuarios u  ON av.id_Usuario_fk  = u.idUsuario
        LEFT JOIN roles r     ON av.id_Rol_fk      = r.idRol
    """)
    resultado = cursor.fetchall()
    con.close()
    return resultado

def crear_atencion(id_vehiculo, id_usuario, id_rol, fecha_inicio, fecha_final):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO atencion_vehiculo (id_Vehiculo_fk, id_Usuario_fk, id_Rol_fk, fecha_inicio, fecha_final) 
        VALUES (%s, %s, %s, %s, %s)
    """, (id_vehiculo, id_usuario, id_rol, fecha_inicio, fecha_final))
    con.commit()
    con.close()

import os
import mysql.connector

def conectar():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", ""),
        database=os.environ.get("DB_NAME", "taller_el_costa")
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

def obtener_usuario_por_correo(correo):
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
    resultado = cursor.fetchone()
    con.close()
    return resultado

def obtener_usuario_por_id(id):
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE idUsuario = %s", (id,))
    resultado = cursor.fetchone()
    con.close()
    return resultado

def actualizar_totp_secret(id, secret):
    # secret = cadena base32 para activar 2FA, o None para desactivarlo
    con = conectar()
    cursor = con.cursor()
    cursor.execute("UPDATE usuarios SET totp_secret=%s WHERE idUsuario=%s", (secret, id))
    con.commit()
    con.close()

def actualizar_contrasena_por_correo(correo, nueva_contrasena):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("UPDATE usuarios SET contraseña=%s WHERE correo=%s", (nueva_contrasena, correo))
    con.commit()
    filas = cursor.rowcount
    con.close()
    return filas

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

def crear_vehiculo(id_usuario, id_marca, placa, modelo, anio, color, tipo):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO vehiculos (id_Usuario_fk, id_Marca_fk, placa, modelo, año, color, tipo)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (id_usuario, id_marca, placa, modelo, anio, color, tipo))
    con.commit()
    nuevo_id = cursor.lastrowid
    con.close()
    return nuevo_id

def obtener_vehiculo_por_placa(placa):
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM vehiculos WHERE placa = %s", (placa,))
    resultado = cursor.fetchone()
    con.close()
    return resultado

def obtener_o_crear_cliente(nombre_completo):
    # Busca un cliente (rol 3) por nombre completo; si no existe, lo crea. Devuelve idUsuario
    nombre_completo = (nombre_completo or '').strip()
    partes = nombre_completo.split(' ', 1)
    nombre   = partes[0]
    apellido = partes[1] if len(partes) > 1 else ''
    con = conectar()
    cursor = con.cursor()
    cursor.execute("""
        SELECT idUsuario FROM usuarios
        WHERE id_Rol_fk = 3
          AND LOWER(TRIM(CONCAT(COALESCE(nombre,''), ' ', COALESCE(apellido,'')))) = LOWER(%s)
        LIMIT 1
    """, (nombre_completo,))
    fila = cursor.fetchone()
    if fila:
        id_usuario = fila[0]
    else:
        cursor.execute(
            "INSERT INTO usuarios (nombre, apellido, id_Rol_fk) VALUES (%s, %s, 3)",
            (nombre, apellido)
        )
        con.commit()
        id_usuario = cursor.lastrowid
    con.close()
    return id_usuario

def obtener_o_crear_marca(nombre):
    # Devuelve el idMarca; si la marca no existe (por nombre) la crea
    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT idMarca FROM marca_vehiculo WHERE LOWER(nombre) = LOWER(%s)", (nombre,))
    fila = cursor.fetchone()
    if fila:
        id_marca = fila[0]
    else:
        cursor.execute("INSERT INTO marca_vehiculo (nombre) VALUES (%s)", (nombre,))
        con.commit()
        id_marca = cursor.lastrowid
    con.close()
    return id_marca

def actualizar_vehiculo(id, id_usuario, id_marca, placa, modelo, anio, color, tipo):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("""
        UPDATE vehiculos SET id_Usuario_fk=%s, id_Marca_fk=%s, placa=%s, modelo=%s, año=%s, color=%s, tipo=%s 
        WHERE IDvehiculos=%s
    """, (id_usuario, id_marca, placa, modelo, anio, color, tipo, id))
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
               v.placa, v.modelo AS modelo_veh,
               mar.nombre AS marca,
               CONCAT(u.nombre, ' ', u.apellido) AS cliente,
               e.nombre AS estado
        FROM orden_servicio os
        LEFT JOIN vehiculos v       ON os.id_Vehiculo_fk = v.IDvehiculos
        LEFT JOIN marca_vehiculo mar ON v.id_Marca_fk    = mar.idMarca
        LEFT JOIN usuarios u        ON os.id_Usuario_fk  = u.idUsuario
        LEFT JOIN estado_orden e    ON os.id_Estado_fk   = e.idEstado
        ORDER BY os.fecha_apertura DESC
    """)
    resultado = cursor.fetchall()
    con.close()
    return resultado

def obtener_ordenes_por_mecanico(id_mecanico):
    # Órdenes de los vehículos que ESTE mecánico ha atendido (solo lo suyo).
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("""
        SELECT os.*,
               v.placa, v.modelo AS modelo_veh,
               mar.nombre AS marca,
               CONCAT(u.nombre, ' ', u.apellido) AS cliente,
               e.nombre AS estado
        FROM orden_servicio os
        LEFT JOIN vehiculos v        ON os.id_Vehiculo_fk = v.IDvehiculos
        LEFT JOIN marca_vehiculo mar ON v.id_Marca_fk     = mar.idMarca
        LEFT JOIN usuarios u         ON os.id_Usuario_fk  = u.idUsuario
        LEFT JOIN estado_orden e     ON os.id_Estado_fk   = e.idEstado
        WHERE os.id_Vehiculo_fk IN (
            SELECT id_Vehiculo_fk FROM atencion_vehiculo WHERE id_Usuario_fk = %s
        )
        ORDER BY os.fecha_apertura DESC
    """, (id_mecanico,))
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

def obtener_siguiente_numero_orden():
    # Devuelve el mayor numero_orden numérico existente + 1 (empieza en 1001 si no hay)
    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT MAX(CAST(numero_orden AS UNSIGNED)) FROM orden_servicio")
    maximo = cursor.fetchone()[0]
    con.close()
    return (maximo or 1000) + 1

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

def actualizar_orden(id_orden, cliente, placa, marca, modelo_txt, fecha):
    # Edita los datos de una orden: nombre del cliente, datos del vehículo y fecha.
    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT id_Vehiculo_fk, id_Usuario_fk FROM orden_servicio WHERE Id_orden=%s", (id_orden,))
    fila = cursor.fetchone()
    if not fila:
        con.close()
        return
    id_veh, id_cli = fila
    # Cliente (nombre completo -> nombre + apellido)
    nombre_completo = (cliente or '').strip()
    partes = nombre_completo.split(' ', 1)
    nombre = partes[0] if partes else ''
    apellido = partes[1] if len(partes) > 1 else ''
    if id_cli:
        cursor.execute("UPDATE usuarios SET nombre=%s, apellido=%s WHERE idUsuario=%s",
                       (nombre, apellido, id_cli))
    # Marca (buscar o crear) y actualizar vehículo
    if id_veh:
        cursor.execute("SELECT idMarca FROM marca_vehiculo WHERE LOWER(nombre)=LOWER(%s)", (marca,))
        m = cursor.fetchone()
        if m:
            id_marca = m[0]
        else:
            cursor.execute("INSERT INTO marca_vehiculo (nombre) VALUES (%s)", (marca,))
            id_marca = cursor.lastrowid
        cursor.execute("UPDATE vehiculos SET placa=%s, id_Marca_fk=%s, modelo=%s WHERE IDvehiculos=%s",
                       (placa, id_marca, modelo_txt, id_veh))
    # Fecha de apertura
    if fecha:
        cursor.execute("UPDATE orden_servicio SET fecha_apertura=%s WHERE Id_orden=%s", (fecha, id_orden))
    con.commit()
    con.close()

def actualizar_precio_orden(id, total):
    # Pone/actualiza solo el precio (total) de la orden, sin cerrarla.
    con = conectar()
    cursor = con.cursor()
    cursor.execute("UPDATE orden_servicio SET total=%s WHERE Id_orden=%s", (total, id))
    con.commit()
    con.close()

def eliminar_orden(id):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("DELETE FROM orden_servicio WHERE Id_orden=%s", (id,))
    con.commit()
    con.close()

def obtener_ordenes_sin_finalizar():
    # Órdenes cuyo estado NO es 'Finalizado' (las que siguen abiertas / en proceso),
    # listas para mostrar en tarjetas (mecánico, cliente, vehículo, productos, total).
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("""
        SELECT os.Id_orden, os.numero_orden, os.fecha_apertura, os.total,
               v.placa, v.modelo, m.nombre AS marca,
               CONCAT(cu.nombre, ' ', COALESCE(cu.apellido, '')) AS cliente,
               e.nombre AS estado,
               (SELECT CONCAT(mu.nombre, ' ', COALESCE(mu.apellido, ''))
                  FROM atencion_vehiculo av
                  JOIN usuarios mu ON av.id_Usuario_fk = mu.idUsuario
                  WHERE av.id_Vehiculo_fk = os.id_Vehiculo_fk
                  ORDER BY av.idAtencion DESC LIMIT 1) AS mecanico
        FROM orden_servicio os
        LEFT JOIN vehiculos v      ON os.id_Vehiculo_fk = v.IDvehiculos
        LEFT JOIN marca_vehiculo m ON v.id_Marca_fk     = m.idMarca
        LEFT JOIN usuarios cu      ON os.id_Usuario_fk  = cu.idUsuario
        LEFT JOIN estado_orden e   ON os.id_Estado_fk   = e.idEstado
        WHERE e.nombre IS NULL OR e.nombre <> 'Finalizado'
        ORDER BY os.fecha_apertura DESC, os.Id_orden DESC
    """)
    filas = cursor.fetchall()
    resultado = []
    for f in filas:
        cursor.execute("""
            SELECT DISTINCT p.nombre_producto
            FROM detalle_orden d
            LEFT JOIN producto p ON d.id_Producto_fk = p.idProducto
            WHERE d.id_Orden_fk = %s AND p.nombre_producto IS NOT NULL
        """, (f['Id_orden'],))
        productos = [r['nombre_producto'] for r in cursor.fetchall()]
        vehiculo = ((f['marca'] or '') + ' ' + (f['modelo'] or '')).strip() or 'Vehículo'
        total = f['total']
        total_str = ('$' + format(int(total), ',')) if total not in (None, '') else '—'
        resultado.append({
            'id': 'OS-' + str(f['numero_orden']),
            'mecanico': (f['mecanico'] or '').strip() or 'Sin asignar',
            'cliente': (f['cliente'] or '').strip() or '—',
            'marca': vehiculo,
            'placa': f['placa'] or '—',
            'productos': productos,
            'total': total_str,
            'estado': 'en_proceso',
            'fecha': str(f['fecha_apertura']) if f['fecha_apertura'] else '',
        })
    con.close()
    return resultado


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
    # Descontar del inventario el producto utilizado (sin bajar de 0)
    if id_producto:
        try:
            cant = int(cantidad or 0)
        except (TypeError, ValueError):
            cant = 0
        if cant > 0:
            cursor.execute("UPDATE producto SET stock = GREATEST(stock - %s, 0) WHERE idProducto=%s",
                           (cant, id_producto))
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

def orden_tiene_factura(id_orden):
    # True si la orden ya fue facturada (para no duplicar facturas).
    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT COUNT(*) FROM factura WHERE id_Orden_fk = %s", (id_orden,))
    n = cursor.fetchone()[0]
    con.close()
    return n > 0

def obtener_siguiente_numero_factura():
    # Devuelve el mayor numero_factura numérico + 1 (empieza en 1000 si no hay).
    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT MAX(CAST(numero_factura AS UNSIGNED)) FROM factura")
    maximo = cursor.fetchone()[0]
    con.close()
    return (maximo or 999) + 1

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
    # Movimientos reales: productos usados en las órdenes (salidas de inventario),
    # con la cantidad gastada y el stock actual de cada producto.
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.nombre_producto AS producto,
               'Salida' AS tipo,
               d.cantidad AS cantidad,
               fa.fecha AS fecha,
               os.numero_orden AS numero_orden,
               fa.numero_factura AS numero_factura,
               p.stock AS stock,
               CONCAT('Factura #', fa.numero_factura, ' · Orden #', os.numero_orden) AS observacion
        FROM detalle_orden d
        JOIN producto p        ON d.id_Producto_fk = p.idProducto
        JOIN orden_servicio os ON d.id_Orden_fk    = os.Id_orden
        JOIN factura fa        ON fa.id_Orden_fk   = os.Id_orden
        ORDER BY fa.fecha DESC, d.idDetalleServicio DESC
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
        ORDER BY av.fecha_inicio DESC, av.idAtencion DESC
    """)
    resultado = cursor.fetchall()
    con.close()
    return resultado

def obtener_atenciones_por_mecanico(id_mecanico):
    # Solo las atenciones asignadas a ESTE mecánico.
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
        WHERE av.id_Usuario_fk = %s
        ORDER BY av.fecha_inicio DESC, av.idAtencion DESC
    """, (id_mecanico,))
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
def validar_usuario(correo, contrasena):

    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    sql = """
        SELECT * 
        FROM usuarios
        WHERE correo = %s
        AND contrasena = %s
    """

    cursor.execute(sql, (correo, contrasena))

    usuario = cursor.fetchone()

    conexion.close()

    return usuario

# ═════════════════════════════════════════
#  ESTADÍSTICAS PARA EXPORTAR
# ═════════════════════════════════════════

def obtener_producto_mas_vendido():
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.nombre_producto, SUM(d.cantidad) AS total_ventas,
               SUM(d.cantidad * d.precio_unitario) AS ingresos
        FROM detalle_orden d
        LEFT JOIN producto p ON d.id_Producto_fk = p.idProducto
        GROUP BY d.id_Producto_fk
        ORDER BY total_ventas DESC
        LIMIT 1
    """)
    resultado = cursor.fetchone()
    con.close()
    return resultado

def obtener_ventas_por_categoria():
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.nombre AS categoria,
               SUM(d.cantidad) AS total_ventas,
               SUM(d.cantidad * d.precio_unitario) AS ingresos
        FROM detalle_orden d
        LEFT JOIN producto p ON d.id_Producto_fk = p.idProducto
        LEFT JOIN categoria_producto c ON p.id_Categoria_fk = c.idCategoria
        GROUP BY c.idCategoria
        ORDER BY total_ventas DESC
    """)
    resultado = cursor.fetchall()
    con.close()
    return resultado

def obtener_actividad_mensual_anio(anio=None):
    # Devuelve un arreglo de 12 posiciones (Ene..Dic) con las órdenes por mes del año dado.
    con = conectar()
    cursor = con.cursor()
    if anio is None:
        cursor.execute("""
            SELECT MONTH(fecha_apertura) AS mes, COUNT(*) AS total
            FROM orden_servicio
            WHERE YEAR(fecha_apertura) = YEAR(CURDATE())
            GROUP BY MONTH(fecha_apertura)
        """)
    else:
        cursor.execute("""
            SELECT MONTH(fecha_apertura) AS mes, COUNT(*) AS total
            FROM orden_servicio
            WHERE YEAR(fecha_apertura) = %s
            GROUP BY MONTH(fecha_apertura)
        """, (anio,))
    datos = [0] * 12
    for mes, total in cursor.fetchall():
        if mes and 1 <= mes <= 12:
            datos[mes - 1] = total
    con.close()
    return datos


def obtener_actividad_mensual():
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("""
        SELECT MONTH(fecha_apertura) AS mes,
               COUNT(*) AS total_ordenes
        FROM orden_servicio
        GROUP BY MONTH(fecha_apertura)
        ORDER BY mes
    """)
    resultado = cursor.fetchall()
    con.close()
    return resultado

def obtener_finanzas_mes(offset=0):
    # Finanzas de un mes (offset relativo al actual): ganancias (facturado ese mes),
    # gastos (entradas de inventario valoradas a precio_compra, con fecha de su factura),
    # y conteos de órdenes y facturas del mes.
    con = conectar()
    cur = con.cursor(dictionary=True)
    cur.execute(
        "SELECT MONTH(DATE_ADD(CURDATE(), INTERVAL %s MONTH)) AS m, "
        "YEAR(DATE_ADD(CURDATE(), INTERVAL %s MONTH)) AS a", (offset, offset))
    r = cur.fetchone()
    mes, anio = r['m'], r['a']

    cur.execute("SELECT COALESCE(SUM(total),0) AS s, COUNT(*) AS c FROM factura "
                "WHERE MONTH(fecha)=%s AND YEAR(fecha)=%s", (mes, anio))
    g = cur.fetchone()
    ganancias = int(g['s'] or 0)
    facturas = g['c']

    cur.execute("SELECT COUNT(*) AS c FROM orden_servicio "
                "WHERE MONTH(fecha_apertura)=%s AND YEAR(fecha_apertura)=%s", (mes, anio))
    ordenes = cur.fetchone()['c']

    cur.execute("""
        SELECT COALESCE(SUM(dm.cantidad * p.precio_compra),0) AS s
        FROM detalle_movimiento dm
        JOIN factura f                  ON dm.id_Factura_fk = f.idFactura
        LEFT JOIN producto_proveedor pp ON dm.id_ProductoProveedor_fk = pp.idProductoProveedor
        LEFT JOIN producto p            ON pp.id_Producto_fk = p.idProducto
        WHERE MONTH(f.fecha)=%s AND YEAR(f.fecha)=%s
    """, (mes, anio))
    gastos = int(cur.fetchone()['s'] or 0)
    con.close()
    return {'mes': mes, 'anio': anio, 'ganancias': ganancias, 'gastos': gastos,
            'ordenes': ordenes, 'facturas': facturas}


def obtener_total_ganancias():
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT SUM(total) AS total FROM factura")
    resultado = cursor.fetchone()
    con.close()
    return resultado['total'] or 0

def obtener_total_gastos():
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT SUM(precio_compra * stock) AS total FROM producto")
    resultado = cursor.fetchone()
    con.close()
    return resultado['total'] or 0

def obtener_mecanico_destacado():
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("""
        SELECT CONCAT(u.nombre, ' ', u.apellido) AS mecanico,
               COUNT(av.idAtencion) AS total_ordenes
        FROM atencion_vehiculo av
        LEFT JOIN usuarios u ON av.id_Usuario_fk = u.idUsuario
        GROUP BY av.id_Usuario_fk
        ORDER BY total_ordenes DESC
        LIMIT 3
    """)
    resultado = cursor.fetchall()
    con.close()
    return resultado

def obtener_ordenes_semana(offset=0):
    # offset = semanas relativas a la actual (0 = esta semana, -1 = la pasada, ...).
    # Devuelve (datos[7] de Lun..Dom, fecha del lunes de esa semana).
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("""
        SELECT DAYOFWEEK(fecha_apertura) AS dia, COUNT(*) AS total
        FROM orden_servicio
        WHERE YEARWEEK(fecha_apertura, 1) = YEARWEEK(DATE_ADD(CURDATE(), INTERVAL %s WEEK), 1)
        GROUP BY DAYOFWEEK(fecha_apertura)
    """, (offset,))
    resultado = cursor.fetchall()
    cursor.execute(
        "SELECT DATE_SUB(DATE_ADD(CURDATE(), INTERVAL %s WEEK), "
        "INTERVAL WEEKDAY(DATE_ADD(CURDATE(), INTERVAL %s WEEK)) DAY) AS lunes",
        (offset, offset))
    lunes = cursor.fetchone()['lunes']
    con.close()
    datos = [0] * 7
    for r in resultado:
        dia = r['dia']
        if dia == 1:
            datos[6] = r['total']      # Domingo (DAYOFWEEK=1) va al final
        else:
            datos[dia - 2] = r['total']
    return datos, lunes


def obtener_ordenes_semana_actual():
    datos, _ = obtener_ordenes_semana(0)
    return datos
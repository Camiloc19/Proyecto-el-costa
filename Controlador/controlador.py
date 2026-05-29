from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Modelo'))
import modelo

app = Flask(__name__, template_folder='../Vista')
app.secret_key = 'taller_el_costa_2026'


# ═════════════════════════════════════════
#  LOGIN
# ═════════════════════════════════════════

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo     = request.form.get('correo')
        contrasena = request.form.get('contrasena')
        usuario    = modelo.login_usuario(correo, contrasena)
        if usuario:
            session['usuario'] = usuario['nombre'] + ' ' + usuario['apellido']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Correo o contraseña incorrectos')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ═════════════════════════════════════════
#  DASHBOARD
# ═════════════════════════════════════════

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


# ═════════════════════════════════════════
#  USUARIOS
# ═════════════════════════════════════════

@app.route('/usuarios')
def usuarios():
    lista = modelo.obtener_usuarios()
    roles = modelo.obtener_roles()
    return render_template('usuarios.html', usuarios=lista, roles=roles)

@app.route('/usuarios/agregar', methods=['POST'])
def agregar_usuario():
    nombre     = request.form.get('nombre')
    apellido   = request.form.get('apellido')
    contrasena = request.form.get('contrasena')
    correo     = request.form.get('correo')
    id_rol     = request.form.get('id_rol')
    modelo.crear_usuario(nombre, apellido, contrasena, correo, id_rol)
    return redirect(url_for('usuarios'))

@app.route('/usuarios/editar/<int:id>', methods=['POST'])
def editar_usuario(id):
    nombre     = request.form.get('nombre')
    apellido   = request.form.get('apellido')
    contrasena = request.form.get('contrasena')
    correo     = request.form.get('correo')
    id_rol     = request.form.get('id_rol')
    modelo.actualizar_usuario(id, nombre, apellido, contrasena, correo, id_rol)
    return redirect(url_for('usuarios'))

@app.route('/usuarios/eliminar/<int:id>')
def eliminar_usuario(id):
    modelo.eliminar_usuario(id)
    return redirect(url_for('usuarios'))


# ═════════════════════════════════════════
#  VEHÍCULOS
# ═════════════════════════════════════════

@app.route('/vehiculos')
def vehiculos():
    lista    = modelo.obtener_vehiculos()
    usuarios = modelo.obtener_usuarios()
    marcas   = modelo.obtener_marcas()
    return render_template('vehiculos.html', vehiculos=lista, usuarios=usuarios, marcas=marcas)

@app.route('/vehiculos/agregar', methods=['POST'])
def agregar_vehiculo():
    id_usuario = request.form.get('id_usuario')
    id_marca   = request.form.get('id_marca')
    placa      = request.form.get('placa')
    mod        = request.form.get('modelo')
    anio       = request.form.get('anio')
    color      = request.form.get('color')
    tipo       = request.form.get('tipo')
    modelo.crear_vehiculo(id_usuario, id_marca, placa, mod, anio, color, tipo)
    return redirect(url_for('vehiculos'))

@app.route('/vehiculos/editar/<int:id>', methods=['POST'])
def editar_vehiculo(id):
    id_usuario = request.form.get('id_usuario')
    id_marca   = request.form.get('id_marca')
    placa      = request.form.get('placa')
    mod        = request.form.get('modelo')
    anio       = request.form.get('anio')
    color      = request.form.get('color')
    tipo       = request.form.get('tipo')
    modelo.actualizar_vehiculo(id, id_usuario, id_marca, placa, mod, anio, color, tipo)
    return redirect(url_for('vehiculos'))

@app.route('/vehiculos/eliminar/<int:id>')
def eliminar_vehiculo(id):
    modelo.eliminar_vehiculo(id)
    return redirect(url_for('vehiculos'))


# ═════════════════════════════════════════
#  INVENTARIO
# ═════════════════════════════════════════

@app.route('/inventario')
def inventario():
    productos  = modelo.obtener_productos()
    categorias = modelo.obtener_categorias()
    return render_template('inventario.html', productos=productos, categorias=categorias)

@app.route('/inventario/agregar', methods=['POST'])
def agregar_producto():
    id_categoria  = request.form.get('id_categoria')
    nombre        = request.form.get('nombre')
    descripcion   = request.form.get('descripcion')
    stock         = request.form.get('stock', 0)
    stock_minimo  = request.form.get('stock_minimo', 0)
    precio_compra = request.form.get('precio_compra', 0)
    precio_venta  = request.form.get('precio_venta', 0)
    modelo.crear_producto(id_categoria, nombre, descripcion, stock, stock_minimo, precio_compra, precio_venta)
    return redirect(url_for('inventario'))

@app.route('/inventario/editar/<int:id>', methods=['POST'])
def editar_producto(id):
    id_categoria  = request.form.get('id_categoria')
    nombre        = request.form.get('nombre')
    descripcion   = request.form.get('descripcion')
    stock         = request.form.get('stock', 0)
    stock_minimo  = request.form.get('stock_minimo', 0)
    precio_compra = request.form.get('precio_compra', 0)
    precio_venta  = request.form.get('precio_venta', 0)
    modelo.actualizar_producto(id, id_categoria, nombre, descripcion, stock, stock_minimo, precio_compra, precio_venta)
    return redirect(url_for('inventario'))

@app.route('/inventario/eliminar/<int:id>')
def eliminar_producto(id):
    modelo.eliminar_producto(id)
    return redirect(url_for('inventario'))


# ═════════════════════════════════════════
#  ÓRDENES DE SERVICIO + ATENCIONES
# ═════════════════════════════════════════

@app.route('/ordenes')
def ordenes():
    lista      = modelo.obtener_ordenes()
    lista_veh  = modelo.obtener_vehiculos()
    lista_usu  = modelo.obtener_usuarios()
    estados    = modelo.obtener_estados_orden()
    atenciones = modelo.obtener_atenciones()
    return render_template('Orden_de_servicio.html',
                           ordenes=lista,
                           vehiculos=lista_veh,
                           usuarios=lista_usu,
                           estados=estados,
                           atenciones=atenciones)

@app.route('/ordenes/agregar', methods=['POST'])
def agregar_orden():
    id_vehiculo    = request.form.get('id_vehiculo')
    id_usuario     = request.form.get('id_usuario')
    id_estado      = request.form.get('id_estado', 1)
    numero_orden   = request.form.get('numero_orden')
    hora_apertura  = request.form.get('hora_apertura')
    fecha_apertura = request.form.get('fecha_apertura')
    modelo.crear_orden(id_vehiculo, id_usuario, id_estado, numero_orden, hora_apertura, fecha_apertura)
    return redirect(url_for('ordenes'))

@app.route('/ordenes/cerrar/<int:id>', methods=['POST'])
def cerrar_orden(id):
    id_estado    = request.form.get('id_estado', 2)
    fecha_cierre = request.form.get('fecha_cierre')
    total        = request.form.get('total', 0)
    modelo.actualizar_estado_orden(id, id_estado, fecha_cierre, total)
    return redirect(url_for('ordenes'))

@app.route('/ordenes/eliminar/<int:id>')
def eliminar_orden(id):
    modelo.eliminar_orden(id)
    return redirect(url_for('ordenes'))

@app.route('/ordenes/detalle/<int:id>')
def detalle_orden(id):
    detalle = modelo.obtener_detalle_orden(id)
    return jsonify(detalle)

@app.route('/ordenes/detalle/agregar', methods=['POST'])
def agregar_detalle():
    id_orden         = request.form.get('id_orden')
    id_tipo_servicio = request.form.get('id_tipo_servicio')
    id_producto      = request.form.get('id_producto')
    cantidad         = request.form.get('cantidad')
    precio_unitario  = request.form.get('precio_unitario')
    modelo.agregar_detalle_orden(id_orden, id_tipo_servicio, id_producto, cantidad, precio_unitario)
    return redirect(url_for('ordenes'))

@app.route('/atenciones/agregar', methods=['POST'])
def agregar_atencion():
    id_vehiculo = request.form.get('id_vehiculo')
    id_usuario  = request.form.get('id_usuario')
    descripcion = request.form.get('descripcion')
    fecha       = request.form.get('fecha')
    modelo.crear_atencion(id_vehiculo, id_usuario, descripcion, fecha)
    return redirect(url_for('ordenes'))


# ═════════════════════════════════════════
#  FACTURACIÓN + MOVIMIENTOS
# ═════════════════════════════════════════

@app.route('/facturacion')
def facturacion():
    facturas         = modelo.obtener_facturas()
    lista_ord        = modelo.obtener_ordenes()
    metodos_pago     = modelo.obtener_metodos_pago()
    movimientos      = modelo.obtener_movimientos()
    productos        = modelo.obtener_productos()
    tipos_movimiento = modelo.obtener_tipos_movimiento()
    return render_template('Facturacion.html',
                           facturas=facturas,
                           ordenes=lista_ord,
                           metodos_pago=metodos_pago,
                           movimientos=movimientos,
                           productos=productos,
                           tipos_movimiento=tipos_movimiento)

@app.route('/facturacion/agregar', methods=['POST'])
def agregar_factura():
    id_orden       = request.form.get('id_orden')
    id_metodo_pago = request.form.get('id_metodo_pago')
    numero_factura = request.form.get('numero_factura')
    fecha          = request.form.get('fecha')
    total          = request.form.get('total')
    modelo.crear_factura(id_orden, id_metodo_pago, numero_factura, fecha, total)
    return redirect(url_for('facturacion'))

@app.route('/movimientos/agregar', methods=['POST'])
def agregar_movimiento():
    id_producto        = request.form.get('id_producto')
    id_tipo_movimiento = request.form.get('id_tipo_movimiento')
    cantidad           = request.form.get('cantidad')
    fecha              = request.form.get('fecha')
    observacion        = request.form.get('observacion')
    modelo.registrar_movimiento(id_producto, id_tipo_movimiento, cantidad, fecha, observacion)
    return redirect(url_for('facturacion'))


# ═════════════════════════════════════════
#  PROVEEDORES
# ═════════════════════════════════════════

@app.route('/proveedores')
def proveedores():
    lista = modelo.obtener_proveedores()
    return render_template('proveedores.html', proveedores=lista)

@app.route('/proveedores/agregar', methods=['POST'])
def agregar_proveedor():
    nombre    = request.form.get('nombre')
    nit       = request.form.get('nit')
    telefono  = request.form.get('telefono')
    direccion = request.form.get('direccion')
    modelo.crear_proveedor(nombre, nit, telefono, direccion)
    return redirect(url_for('proveedores'))

@app.route('/proveedores/editar/<int:id>', methods=['POST'])
def editar_proveedor(id):
    nombre    = request.form.get('nombre')
    nit       = request.form.get('nit')
    telefono  = request.form.get('telefono')
    direccion = request.form.get('direccion')
    modelo.actualizar_proveedor(id, nombre, nit, telefono, direccion)
    return redirect(url_for('proveedores'))

@app.route('/proveedores/eliminar/<int:id>')
def eliminar_proveedor(id):
    modelo.eliminar_proveedor(id)
    return redirect(url_for('proveedores'))


# ═════════════════════════════════════════
#  ESTADÍSTICAS
# ═════════════════════════════════════════

@app.route('/estadisticas')
def estadisticas():
    productos  = modelo.obtener_productos()
    lista_ord  = modelo.obtener_ordenes()
    facturas   = modelo.obtener_facturas()
    bajo_stock = modelo.obtener_productos_bajo_stock()
    return render_template('estadisticas.html',
                           productos=productos,
                           ordenes=lista_ord,
                           facturas=facturas,
                           bajo_stock=bajo_stock)

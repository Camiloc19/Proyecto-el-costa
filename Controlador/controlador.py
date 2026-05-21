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
        correo    = request.form.get('correo')
        contrasena = request.form.get('contrasena')
        usuario   = modelo.login_usuario(correo, contrasena)
        if usuario:
            session['usuario'] = usuario
            return redirect(url_for('inventario'))
        else:
            return render_template('login.html', error='Correo o contraseña incorrectos')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ═════════════════════════════════════════
#  INVENTARIO
# ═════════════════════════════════════════

@app.route('/inventario')
def inventario():
    productos = modelo.obtener_productos()
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
#  ÓRDENES DE SERVICIO
# ═════════════════════════════════════════

@app.route('/ordenes')
def ordenes():
    ordenes    = modelo.obtener_ordenes()
    vehiculos  = modelo.obtener_vehiculos()
    usuarios   = modelo.obtener_usuarios()
    estados    = modelo.obtener_estados_orden()
    return render_template('Orden_de_servicio.html',
                           ordenes=ordenes,
                           vehiculos=vehiculos,
                           usuarios=usuarios,
                           estados=estados)

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
    id_estado   = request.form.get('id_estado', 2)
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
    detalle   = modelo.obtener_detalle_orden(id)
    productos = modelo.obtener_productos()
    tipos     = modelo.obtener_tipos_servicio()
    return jsonify(detalle)

@app.route('/ordenes/detalle/agregar', methods=['POST'])
def agregar_detalle():
    id_orden          = request.form.get('id_orden')
    id_tipo_servicio  = request.form.get('id_tipo_servicio')
    id_producto       = request.form.get('id_producto')
    cantidad          = request.form.get('cantidad')
    precio_unitario   = request.form.get('precio_unitario')
    modelo.agregar_detalle_orden(id_orden, id_tipo_servicio, id_producto, cantidad, precio_unitario)
    return redirect(url_for('ordenes'))


# ═════════════════════════════════════════
#  FACTURACIÓN
# ═════════════════════════════════════════

@app.route('/facturacion')
def facturacion():
    facturas      = modelo.obtener_facturas()
    ordenes       = modelo.obtener_ordenes()
    metodos_pago  = modelo.obtener_metodos_pago()
    return render_template('Facturacion.html',
                           facturas=facturas,
                           ordenes=ordenes,
                           metodos_pago=metodos_pago)

@app.route('/facturacion/agregar', methods=['POST'])
def agregar_factura():
    id_orden        = request.form.get('id_orden')
    id_metodo_pago  = request.form.get('id_metodo_pago')
    numero_factura  = request.form.get('numero_factura')
    fecha           = request.form.get('fecha')
    total           = request.form.get('total')
    modelo.crear_factura(id_orden, id_metodo_pago, numero_factura, fecha, total)
    return redirect(url_for('facturacion'))


# ═════════════════════════════════════════
#  PROVEEDORES
# ═════════════════════════════════════════

@app.route('/proveedores')
def proveedores():
    proveedores = modelo.obtener_proveedores()
    return render_template('proveedores.html', proveedores=proveedores)

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
    ordenes    = modelo.obtener_ordenes()
    facturas   = modelo.obtener_facturas()
    bajo_stock = modelo.obtener_productos_bajo_stock()
    return render_template('estadisticas.html',
                           productos=productos,
                           ordenes=ordenes,
                           facturas=facturas,
                           bajo_stock=bajo_stock)

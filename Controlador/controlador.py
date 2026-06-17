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
            session['id_rol']  = usuario['id_rol_fk']     
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

MODULOS_POR_ROL = {
    1: ['inventario', 'ordenes', 'facturacion', 'proveedores', 'estadisticas'],  # Super_administrador
    2: ['inventario', 'ordenes', 'facturacion', 'proveedores', 'estadisticas'],  # Administrador
    3: [],                                                                         # Cliente (sin acceso)
    4: ['ordenes'],                                                                # Mecánico
}

@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    permitidos = MODULOS_POR_ROL.get(session.get('id_rol'), [])
    return render_template('dashboard.html', modulos=permitidos)

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
    semana     = modelo.obtener_ordenes_semana_actual()
    return render_template('estadisticas.html',
                           productos=productos,
                           ordenes=lista_ord,
                           facturas=facturas,
                           bajo_stock=bajo_stock,
                           semana=semana)

## ═════════════════════════════════════════
#  EXPORTAR EXCEL Y PDF
# ═════════════════════════════════════════
from flask import send_file
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

@app.route('/exportar-excel')
def exportar_excel():
    wb = openpyxl.Workbook()

    # ── Hoja 1: Producto más vendido ──
    ws1 = wb.active
    ws1.title = "Producto Más Vendido"
    ws1.append(["Producto", "Ventas Totales", "Ingresos"])
    pm = modelo.obtener_producto_mas_vendido()
    if pm:
        ws1.append([pm['nombre_producto'], pm['total_ventas'], float(pm['ingresos'])])

    # ── Hoja 2: Ventas por Categoría ──
    ws2 = wb.create_sheet("Categorías")
    ws2.append(["Categoría", "Ventas", "Ingresos"])
    for c in modelo.obtener_ventas_por_categoria():
        ws2.append([c['categoria'], c['total_ventas'], float(c['ingresos'])])

    # ── Hoja 3: Actividad Mensual ──
    ws3 = wb.create_sheet("Actividad Mensual")
    meses = {1:'Enero',2:'Febrero',3:'Marzo',4:'Abril',5:'Mayo',6:'Junio',
             7:'Julio',8:'Agosto',9:'Septiembre',10:'Octubre',11:'Noviembre',12:'Diciembre'}
    ws3.append(["Mes", "Órdenes"])
    for m in modelo.obtener_actividad_mensual():
        ws3.append([meses.get(m['mes'], m['mes']), m['total_ordenes']])

    # ── Hoja 4: Ganancias y Gastos ──
    ws4 = wb.create_sheet("Ganancias y Gastos")
    ws4.append(["Concepto", "Total"])
    ws4.append(["Total Ganancias", float(modelo.obtener_total_ganancias())])
    ws4.append(["Total Gastos",    float(modelo.obtener_total_gastos())])

    # ── Hoja 5: Mecánicos Destacados ──
    ws5 = wb.create_sheet("Mecánicos")
    ws5.append(["Mecánico", "Órdenes Atendidas"])
    for m in modelo.obtener_mecanico_destacado():
        ws5.append([m['mecanico'], m['total_ordenes']])

    # ── Hoja 6: Órdenes ──
    ws6 = wb.create_sheet("Órdenes")
    ws6.append(["N° Orden", "Cliente", "Vehículo", "Fecha Apertura", "Fecha Cierre", "Estado", "Total"])
    for o in modelo.obtener_ordenes():
        ws6.append([o['numero_orden'], o['cliente'], o['placa'],
                    str(o['fecha_apertura']), str(o['fecha_cierre']),
                    o['estado'], float(o['total'] or 0)])

    # ── Hoja 7: Facturas ──
    ws7 = wb.create_sheet("Facturas")
    ws7.append(["N° Factura", "Orden", "Fecha", "Método Pago", "Total"])
    for f in modelo.obtener_facturas():
        ws7.append([f['numero_factura'], f['numero_orden'],
                    str(f['fecha']), f['metodo_pago'], float(f['total'])])

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return send_file(output, download_name="reporte_taller_el_costa.xlsx", as_attachment=True)


@app.route('/exportar-pdf')
def exportar_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    naranja = colors.HexColor('#f97316')

    # Título
    elements.append(Paragraph("Reporte General — Taller El Costa", styles['Title']))
    elements.append(Spacer(1, 12))

    # ── Producto más vendido ──
    elements.append(Paragraph("Producto Más Vendido", styles['Heading2']))
    pm = modelo.obtener_producto_mas_vendido()
    if pm:
        data = [["Producto", "Ventas Totales", "Ingresos"],
                [pm['nombre_producto'], pm['total_ventas'], f"${float(pm['ingresos']):,.0f}"]]
        t = Table(data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), naranja),
            ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
            ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f5f5f5')]),
        ]))
        elements.append(t)
    elements.append(Spacer(1, 12))

    # ── Ventas por Categoría ──
    elements.append(Paragraph("Ventas por Categoría", styles['Heading2']))
    data = [["Categoría", "Ventas", "Ingresos"]]
    for c in modelo.obtener_ventas_por_categoria():
        data.append([c['categoria'], c['total_ventas'], f"${float(c['ingresos']):,.0f}"])
    t = Table(data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), naranja),
        ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f5f5f5'), colors.white]),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 12))

    # ── Ganancias y Gastos ──
    elements.append(Paragraph("Ganancias y Gastos", styles['Heading2']))
    data = [["Concepto", "Total"],
            ["Total Ganancias", f"${float(modelo.obtener_total_ganancias()):,.0f}"],
            ["Total Gastos",    f"${float(modelo.obtener_total_gastos()):,.0f}"]]
    t = Table(data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), naranja),
        ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f5f5f5'), colors.white]),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 12))

    # ── Mecánicos Destacados ──
    elements.append(Paragraph("Top Mecánicos", styles['Heading2']))
    data = [["Mecánico", "Órdenes Atendidas"]]
    for m in modelo.obtener_mecanico_destacado():
        data.append([m['mecanico'], m['total_ordenes']])
    t = Table(data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), naranja),
        ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f5f5f5'), colors.white]),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 12))

    # ── Órdenes ──
    elements.append(Paragraph("Órdenes de Servicio", styles['Heading2']))
    data = [["N° Orden", "Cliente", "Placa", "Fecha", "Estado", "Total"]]
    for o in modelo.obtener_ordenes():
        data.append([o['numero_orden'], o['cliente'], o['placa'],
                     str(o['fecha_apertura']), o['estado'],
                     f"${float(o['total'] or 0):,.0f}"])
    t = Table(data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), naranja),
        ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f5f5f5'), colors.white]),
        ('FONTSIZE', (0,0), (-1,-1), 8),
    ]))
    elements.append(t)

    doc.build(elements)
    buffer.seek(0)
    return send_file(buffer, download_name="reporte_taller_el_costa.pdf", as_attachment=True)
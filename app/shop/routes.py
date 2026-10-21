from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from app.models import Producto, Categoria
from app.extensions import db

shop_bp = Blueprint('shop', __name__)

@shop_bp.route('/')
def tienda():
    # Obtener filtros de la URL
    categoria_id = request.args.get('categoria', type=int)
    tipo_cafe = request.args.get('tipo')
    busqueda = request.args.get('q')
    orden = request.args.get('orden')

    query = Producto.query.filter_by(activo=True)

    if categoria_id:
        query = query.filter_by(categoria_id=categoria_id)
    if tipo_cafe:
        query = query.filter_by(tipo_cafe=tipo_cafe)
    if busqueda:
        query = query.filter(Producto.nombre.ilike(f'%{busqueda}%'))

    # Ordenamiento
    if orden == 'precio_asc':
        query = query.order_by(Producto.precio.asc())
    elif orden == 'precio_desc':
        query = query.order_by(Producto.precio.desc())
    elif orden == 'nombre':
        query = query.order_by(Producto.nombre.asc())

    productos = query.all()
    categorias = Categoria.query.all()

    return render_template('tienda.html', productos=productos, categorias=categorias)

@shop_bp.route('/producto/<int:id>')
def detalle_producto(id):
    producto = Producto.query.get_or_404(id)
    return render_template('producto.html', producto=producto)

# Carrito de Compras Básico basado en Sesión
@shop_bp.route('/carrito')
def ver_carrito():
    carrito = session.get('carrito', {})
    productos_en_carrito = []
    subtotal_general = 0

    for producto_id, cantidad in carrito.items():
        producto = Producto.query.get(int(producto_id))
        if producto:
            subtotal = float(producto.precio) * cantidad
            subtotal_general += subtotal
            productos_en_carrito.append({
                'producto': producto,
                'cantidad': cantidad,
                'subtotal': subtotal
            })

    return render_template('carrito.html', items=productos_en_carrito, total=subtotal_general)

@shop_bp.route('/carrito/agregar/<int:producto_id>', methods=['POST'])
def agregar_carrito(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    cantidad = int(request.form.get('cantidad', 1))

    if producto.stock < cantidad:
        flash('No hay suficiente stock disponible.', 'danger')
        return redirect(url_for('shop.detalle_producto', id=producto_id))

    carrito = session.get('carrito', {})
    
    if str(producto_id) in carrito:
        carrito[str(producto_id)] += cantidad
    else:
        carrito[str(producto_id)] = cantidad

    session['carrito'] = carrito
    flash(f'¡{producto.nombre} agregado al carrito!', 'success')
    return redirect(url_for('shop.ver_carrito'))

@shop_bp.route('/carrito/eliminar/<int:producto_id>')
def eliminar_carrito(producto_id):
    carrito = session.get('carrito', {})
    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
        session['carrito'] = carrito
        flash('Producto eliminado del carrito.', 'info')
    return redirect(url_for('shop.ver_carrito'))
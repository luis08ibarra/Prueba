from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from app.models import Producto, Pedido, Usuario

admin_bp = Blueprint('admin', __name__)

@admin_bp.before_request
@login_required
def verificar_admin():
    if current_user.rol != 'admin':
        abort(403) # Acceso prohibido si no es administrador

@admin_bp.route('/')
def dashboard():
    total_productos = Producto.query.count()
    total_pedidos = Pedido.query.count()
    total_usuarios = Usuario.query.filter_by(rol='cliente').count()
    pedidos_recientes = Pedido.query.order_by(Pedido.fecha_pedido.desc()).limit(5).all()

    return render_template('admin/dashboard.html', 
                           total_productos=total_productos, 
                           total_pedidos=total_pedidos, 
                           total_usuarios=total_usuarios, 
                           pedidos_recientes=pedidos_recientes)
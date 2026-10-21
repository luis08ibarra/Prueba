from flask import Blueprint, render_template
from app.models import Producto

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Obtener algunos productos destacados de la base de datos para mostrarlos en el inicio
    productos_destacados = Producto.query.filter_by(activo=True).limit(6).all()
    return render_template('index.html', productos=productos_destacados)

@main_bp.route('/contacto')
def contacto():
    return render_template('contacto.html')
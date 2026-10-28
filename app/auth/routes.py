from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import Usuario
from app.extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        password = request.form.get('password')

        usuario_existente = Usuario.query.filter_by(correo=correo).first()
        if usuario_existente:
            flash('El correo electrónico ya está registrado.', 'danger')
            return redirect(url_for('auth.registro'))

        nuevo_usuario = Usuario(nombre_completo=nombre, correo=correo, rol='cliente')
        nuevo_usuario.set_password(password)

        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('¡Registro exitoso! Por favor inicia sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('registro.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        correo = request.form.get('correo')
        password = request.form.get('password')

        usuario = Usuario.query.filter_by(correo=correo).first()

        if usuario and usuario.check_password(password):
            login_user(usuario)
            flash(f'¡Bienvenido de nuevo, {usuario.nombre_completo}!', 'success')
            
            if usuario.rol == 'admin':
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('main.index'))
        else:
            flash('Correo o contrase    ña incorrectos.', 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html')
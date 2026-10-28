from flask import Flask
from config import Config
from app.extensions import db, login_manager
from app.models import Usuario

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Registrar Blueprints
    from app.main.routes import main_bp
    from app.auth.routes import auth_bp
    from app.shop.routes import shop_bp
    from app.admin.routes import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(shop_bp, url_prefix='/tienda')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app
from .authController import auth_bp
from .adminController import admin_bp
from .appUserController import user_bp

def register_controller(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)

from flask import Flask
from flask_login import LoginManager
from config import Config
from database import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Инициализация базы данных
    db.init_app(app)

    # Инициализация Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Регистрация Blueprints
    from app.controllers.auth_controller import auth_bp
    from app.controllers.product_controller import product_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)

    # Импорт моделей для создания таблиц
    from app.models.user import User
    from app.models.product import Product

    # Создание таблиц
    with app.app_context():
        db.create_all()

    # Функция загрузки пользователя для Flask-Login
    from app.models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app